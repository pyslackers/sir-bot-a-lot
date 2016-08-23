import json

import aiohttp
import asyncio

import sys


class Bot(object):
    def __init__(self, token):
        self.token = token
        self.root_url = 'https://slack.com/api/'
        self.channel = asyncio.Queue()
        self.plugin_manager = []
        print(self.token)

    async def message_parser(self):
        while True:
            message = await self.channel.get()

            if message.get('type') == 'message':
                user = await self.api_call('users.info',
                                      {'user': message.get('user')})

                print('{0}: {1}'.format(user['user']['name'],
                                        message['text']))
            else:
                print(message, file=sys.stderr)

    async def api_call(self, method, data=None):
        with aiohttp.ClientSession() as session:
            form = aiohttp.FormData(data or {})
            form.add_field('token', self.token)
            async with session.post('{0}/{1}'.format(self.root_url, method),
                                    data=form) as response:
                assert 200 == response.status, ('{0} with {1} failed.'
                                               .format(method, data))
                print(response)
                return await response.json()

    async def slack_rtm(self):
        self.rtm = await self.api_call('rtm.start')
        assert self.rtm['ok'], 'Error connecting to RTM.'

        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(self.rtm['url']) as ws:
                async for msg in ws:
                    assert msg.tp == aiohttp.MsgType.text
                    message = json.loads(msg.data)
                    # asyncio.ensure_future(self.consumer(message))
                    await self.channel.put(message)


    def run(self):
        loop = asyncio.get_event_loop()
        loop.set_debug(True)

        loop.run_until_complete(asyncio.wait((self.slack_rtm(),
                                             self.message_parser())))
        loop.close()
