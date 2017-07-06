import asyncio

from sirbot.core.plugin import Plugin
from sirbot.core.hookimpl import hookimpl


class PluginTest(Plugin):
    __name__ = 'test'

    def __init__(self, loop):
        super().__init__(loop)
        self.loop = loop
        self._started = False

    async def configure(self, config, router, session, registry):
        self.config = config

    async def start(self):
        await asyncio.sleep(0.1, loop=self.loop)
        self._started = True

    def facade(self):
        return FacadeTest()

    @property
    def started(self):
        return self._started


class FacadeTest:
    def __init__(self):
        pass


@hookimpl
def plugins(loop):
    return PluginTest(loop)
