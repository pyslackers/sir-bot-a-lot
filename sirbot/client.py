import asyncio
import json
import logging
from urllib.parse import urlencode

import aiohttp
import websockets

log = logging.getLogger(__name__)


class SlackConnectionError(Exception):
    """Connection to Slack Error"""


class HTTPClient:
    pass


class Client:
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
        post_data = urlencode(post_data)

        url = self.make_api_url(method)
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}

        response = await self.session.post(url, data=post_data.encode(),
                                           headers=headers)

        if response.status != 200:
            raise SlackConnectionError('There was a slack connection error')

        message = await response.json()

        return message

    def make_api_url(self, method):
        return self.api_root.format(method)

    async def rtm_connect(self, reconnect=False):
        method = 'rtm.start'
        self._login_data = await self.api_call(method)

        if self._login_data.get('ok'):
            ws_url = self._login_data['url']
            self.ws = await websockets.connect(ws_url)
            print('login data ok')

            while not self.is_closed:
                msg = await self.ws.recv()

                if msg is None:
                    break

                msg = json.loads(msg)

                if msg.get('type') == 'message':
                    print(msg)
                    await self.queue.put(msg)
        else:
            raise Exception('Error with slack {}'.format(self._login_data) )

    async def post_message(self, channel_name_or_id, text):
        data = {
            'type': 'message',
            'channel': channel_name_or_id,
            'text': text
        }
        content = json.dumps(data)
        await self.ws.send(content)

    def run(self):
        try:
            self.loop.run_until_complete(self.rtm_connect())
        except KeyboardInterrupt:
            pass
        finally:
            self.loop.close()
