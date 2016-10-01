import asyncio
import json
import logging
from urllib.parse import urlencode

import aiohttp
import websockets

from .base import Channel

logger = logging.getLogger('sirbot')


class SlackClientError(Exception):
    """Generic slack client error"""


class SlackConnectionError(SlackClientError):
    """Connection to slack server error"""


class SlackServerError(SlackClientError):
    """Internal slack server error"""


class SlackRedirectionError(SlackClientError):
    """Redirection status code"""


class SlackAPIError(SlackClientError):
    """Wrong use of slack API"""


class HTTPClient:
    def __init__(self, token, *, loop=None):
        self.api_root = 'https://slack.com/api/{0}'
        self.api_post_msg = self.api_root.format('chat.postMessage')
        self.api_update_msg = self.api_root.format('chat.update')
        self.api_delete_msg = self.api_root.format('chat.delete')
        self.api_add_react = self.api_root.format('reactions.add')
        self.api_delete_react = self.api_root.format('reactions.remove')
        self.api_get_react = self.api_root.format('reactions.get')
        self.api_get_channel = self.api_root.format('channels.list')
        self.token = token
        self.session = aiohttp.ClientSession()
        self.loop = loop or asyncio.get_event_loop()

    async def delete(self, message):
        logger.debug('Message Delete: {}'.format(message))
        msg = message.serialize()
        msg['token'] = self.token
        rep = await self._post_message(msg, self.api_delete_msg)
        return rep.get('ts')

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

        msg = self._prepare_send_message(message, timestamp)
        rep = await self._post_message(msg, url)
        return rep.get('ts')

    def _prepare_send_message(self, message, timestamp):
        msg = message.serialize()
        msg['token'] = self.token
        if timestamp:
            msg['ts'] = timestamp

        return msg

    async def _post_message(self, msg, url):
        async with self.session.post(url, data=msg) as response:
            if 200 <= response.status < 300:
                rep = await response.json()
                if rep['ok'] is True:
                    logger.debug('Message API response: {}'.format(rep))
                    return rep
                else:
                    logger.warning('Message API response: {}'.format(rep))
                    raise SlackAPIError(rep)
            elif 300 <= response.status < 400:
                e = 'Redirection, status code: {}'.format(response.status)
                logging.error(e)
                raise SlackRedirectionError(e)
            elif 400 <= response.status < 500:
                e = 'Client error, status code: {}'.format(response.status)
                logging.error(e)
                raise SlackConnectionError(e)
            elif 500 <= response.status < 600:
                e = 'Server error, status code: {}'.format(response.status)

    async def add_reaction(self, message, reaction='thumbsup'):
        msg = self._prepare_reaction(message, reaction)
        logger.debug('Reaction Add: {}'.format(msg))
        await self._post_message(msg, self.api_add_react)

    async def delete_reaction(self, message, reaction):
        msg = self._prepare_reaction(message, reaction)
        logger.debug('Reaction Delete: {}'.format(msg))
        await self._post_message(msg, self.api_delete_react)

    async def get_reaction(self, message):
        msg = self._prepare_reaction(message)
        msg['full'] = True
        logger.debug('Reaction Get: {}'.format(msg))
        rep = await self._post_message(msg, self.api_get_react)
        return rep.get('message').get('reactions')

    async def get_channels(self):
        logging.debug('Getting channels')
        all_channels = []
        bot_channels = []

        msg = {'token': self.token}
        rep = await self._post_message(msg, self.api_get_channel)
        for chan in rep.get('channels'):
            channel = Channel(channel_id=chan['id'], **chan)
            all_channels.append(channel)
            if chan.get('is_member'):
                bot_channels.append(channel)

        return bot_channels, all_channels

    def _prepare_reaction(self, message, reaction=''):
        msg = message.serialize()
        msg['token'] = self.token
        msg['name'] = reaction
        msg['timestamp'] = msg['ts']
        return msg


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

            while not self.is_closed:
                msg = await self.ws.recv()
                if msg is None:
                    break

                msg = json.loads(msg)
                msg_type = msg.get('type')
                ok = msg.get('ok')

                if msg_type == 'hello':
                    logger.debug('login data ok')
                elif msg_type == 'message':
                    logger.debug('Message Received: %s', msg)
                elif ok is True:
                    logger.debug('API response: %s', msg)
                elif ok is False:
                    logger.warning('API error: %s, %s', msg.get('error'), msg)
                else:
                    logger.debug('Event Received: %s', msg)

                await self.queue.put(msg)

        else:
            raise SlackConnectionError(
                'Error with slack {}'.format(self._login_data))

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
