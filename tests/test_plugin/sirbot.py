from sirbot.hookimpl import hookimpl
from sirbot.plugin import Plugin


class PluginTest(Plugin):
    def __init__(self, loop):
        super().__init__(loop)
        self.loop = loop

    def configure(self, config, router, facades):
        self.config = config

    async def start(self):
        pass

    def facade(self):
        return FacadeTest()


class FacadeTest:
    def __init__(self):
        pass


@hookimpl
def plugins(loop):
    return 'test', PluginTest(loop)
