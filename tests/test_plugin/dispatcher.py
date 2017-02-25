from .facade import TestFacade


class Dispatcher:
    def __init__(self, loop):
        self.loop = loop
        self._config = None
        self.msg = list()

    async def incoming(self, msg, chat, facade):
        self.msg.append((msg, chat, facade))
        if msg == 'error':
            raise Exception

    def configure(self, config):
        self._config = config

    def facade(self):
        return TestFacade()
