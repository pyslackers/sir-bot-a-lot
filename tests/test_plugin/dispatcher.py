from .facade import TestFacade


class Dispatcher:
    def __init__(self, loop, config):
        self.loop = loop
        self.config = config
        self.msg = list()

    async def incoming(self, msg, chat, facade):
        self.msg.append((msg, chat, facade))
        if msg == 'error':
            raise Exception

    def facade(self):
        return TestFacade()
