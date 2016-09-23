import asyncio
import json
import logging
from urllib.parse import urlencode

import aiohttp
import websockets

logger = logging.getLogger('sirbot')


class SlackConnectionError(Exception):
    """Connection to Slack Error"""


class HTTPClient:
    def __init__(self, token, *, loop=None):
        self.api_root = 'https://slack.com/api/{0}'
        self.api_post_msg = self.api_root.format('chat.postMessage')
        self.api_update_msg = self.api_root.format('chat.update')
        self.token = token
        self.session = aiohttp.ClientSession()
        self.loop = loop or asyncio.get_event_loop()

    async def send(self, message, method='send', timestamp=None):
        if method == 'send':
            logger.debug('Message Sent: {}'.format(message))
            url = self.api_post_msg
        elif method == 'update':
            logger.debug('Message Update: {}'.format(message))
            url = self.api_update_msg
        else:
            logger.warning('Invalid method')
            raise SlackConnectionError

        msg = self._prepare_message(message, timestamp)
        message.timestamp = await self._send_message(msg, url)

    def _prepare_message(self, message, timestamp):
        msg = message.serialize()
        msg['token'] = self.token
        if msg.get('text') is None and msg.get('attachments') is None:
            logger.debug('Can not send msg. No text or attachments.')
            raise SlackConnectionError('No text or attachments')
        if timestamp:
            msg['ts'] = timestamp

        return msg

    async def _send_message(self, msg, url):
        async with self.session.post(url, data=msg) as response:
            if 200 <= response.status < 300:
                rep = await response.json()
                if rep['ok'] is True:
                    logger.debug('Message API response: {}'.format(rep))
                elif rep['ok'] is False:
                    logger.warning(
                        'Can not send message:'
                        '{}, {}'.format(rep.get('error'), rep))
                return rep.get('ts')
            elif 400 <= response.status < 500:
                e = 'There was a slack client error: ' \
                    '{}'.format(response.status)
                logging.error(e)
                raise SlackConnectionError(e)
            elif 400 <= response.status:
                e = 'There was a slack server error: ' \
                    '{}'.format(response.status)
                logging.error(e)
                raise SlackConnectionError(e)
            else:
                e = 'There was a slack unknown error: ' \
                    '{}'.format(response.status)
                logging.error(e)
                raise SlackConnectionError(e)


class RTMClient:
    def __init__(self, token, *, loop=None):
        self.ws = None
        self.loop = loop or asyncio.get_event_loop()
        self.api_root = 'https://slack.com/api/{0}'
        self.message_id = 0
        self.token = token
        self.queue = asyncio.Queue()
        self.session = aiohttp.ClientSession()
        self._login_data = None

        self._closed = asyncio.Event(loop=self.loop)

    def __del__(self):
        self.session.close()

    @property
    def is_closed(self):
        """bool: Indicates if the websocket connection is closed."""
        return self._closed.is_set()

    async def api_call(self, method='?', post_data=None):
        post_data = post_data or {}
        post_data['token'] = self.token
        post_data = urlencode(post_data).encode()

        url = self.make_api_url(method)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
        }

        async with self.session.post(url, data=post_data,
                                     headers=headers) as resp:
            if resp.status != 200:
                logger.error('Unable to post to slack: %s', await resp.text())
                raise SlackConnectionError('Slack connection error')
            return await resp.json()

    def make_api_url(self, method):
        return self.api_root.format(method)

    async def rtm_connect(self, reconnect=False):
        method = 'rtm.start'
        self._login_data = await self.api_call(method)

        if self._login_data.get('ok'):
            ws_url = self._login_data['url']
            self.ws = await websockets.connect(ws_url)
            logger.debug('login data ok')

            while not self.is_closed:
                msg = await self.ws.recv()

                if msg is None:
                    break

                msg = json.loads(msg)
                if msg.get('type') == 'message':
                    logger.debug('Message Received: %s', msg)
                    await self.queue.put(msg)
                elif msg.get('ok') is True:
                    logger.debug('Message API response: {}'.format(msg))
                elif msg.get('ok') is False:
                    logger.warning(
                        'Can not send message:{}, {}'.format(msg.get('error'),
                                                             msg))
        else:
            raise Exception('Error with slack {}'.format(self._login_data))

    async def send_message(self, message, method='send', *args, **kwargs):
        if method == 'update':
            logger.warning('RTMClient does not support message update')
        data = {
            'type': 'message',
            'channel': message.to.id,
            'text': message.text
        }
        logger.debug('Message Sent: {}'.format(message))
        await self.ws.send(json.dumps(data))

    def run(self):
        try:
            self.loop.run_until_complete(self.rtm_connect())
        except KeyboardInterrupt:
            pass
        finally:
            self.loop.close()
