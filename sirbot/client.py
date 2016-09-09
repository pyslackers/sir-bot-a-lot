import asyncio
import json
import logging
from urllib.parse import urlencode
from urllib.request import urlopen

import websockets as websockets

log = logging.getLogger(__name__)


class SlackConnectionError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class HTTPClient:
    pass


class Client:
    def __init__(self, token, *, loop=None, **options):
        self.ws = None
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.api_root = 'https://slack.com/api/{0}'
        self.message_id = 0
        self.token = token
        self.queue = asyncio.Queue()

        self._closed = asyncio.Event(loop=self.loop)

    @property
    def is_closed(self):
        """bool: Indicates if the websocket connection is closed."""
        return self._closed.is_set()

    async def api_call(self, method='?', post_data={}):
        post_data['token'] = self.token
        post_data = urlencode(post_data)

        url = await self.make_api_url(method)

        response = await self.loop.run_in_executor(
            None, urlopen, url, post_data.encode('utf-8'))

        if response.code != 200:
            raise SlackConnectionError('There was a slack connection error')

        message = json.loads(response.read().decode('utf-8'))

        return message

    async def make_api_url(self, method):
        return self.api_root.format(method)

    async def rtm_connect(self, reconnect=False):
        method = 'rtm.start'
        self._login_data = await self.api_call(method)

        if self._login_data['ok']:
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
            self.loop.close()

