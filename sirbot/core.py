import logging
import re
import asyncio
import functools

from .client import Client

logger = logging.getLogger(__name__)


class SirBot:

    def __init__(self, token, *, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self._rtm_client = Client(token)
        self.commands = {
            'listen': {}
        }
        self.mentioned_regex = re.compile(
            r'^(?:\<@(?P<atuser>\w+)\>:?|(?P<username>\w+)) ?(?P<text>.*)$')

        # These are for future purposes. HTTPClient is to send messages via
        # the http api.
        # The webserver is to allow for webhooks and/or web frontend.
        # This will probably be built with aiohttp.

        # self._http_client = HTTPClient(token)
        # self._web_server = WebServer()

    @property
    def bot_id(self):
        return self._rtm_client._login_data['self']['id']

    def listen(self, matchstr, flags=0, func=None):
        if func is None:
            return functools.partial(self.listen, matchstr, flags)
        wrapped = func

        if not asyncio.iscoroutinefunction(wrapped):
            wrapped = asyncio.coroutine(wrapped)
        self.commands['listen'][re.compile(matchstr, flags)] = func

        # Return original func
        return func

    async def rtm_read(self):

        while True:
            msg = await self._rtm_client.queue.get()

            # Don't do anything if the message is an edit or delete
            subtype = msg.get('subtype', '')
            if subtype == u'message_changed':
                continue

            text = msg.get('text', '')
            channel = msg.get('channel', '')

            m = self.mentioned_regex.match(text)

            if m:
                matches = m.groupdict()

                atuser = matches.get('atuser')
                # username = matches.get('username')
                text = matches.get('text')
                # alias = matches.get('alias')

                if atuser != self.bot_id:
                    continue

                for matcher, func in self.commands['listen'].items():
                    n = matcher.search(text)
                    if n:
                        msg = dict(
                            text=text,
                            channel=channel
                        )
                        await func(msg, n.groups())

    def run(self):
        try:
            asyncio.ensure_future(self._rtm_client.rtm_connect(),
                                  loop=self.loop)
            asyncio.ensure_future(self.rtm_read(), loop=self.loop)
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.loop.close()
