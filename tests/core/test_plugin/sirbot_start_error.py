import asyncio

from sirbot.core.hookimpl import hookimpl

from .sirbot import PluginTest


class PluginTestStartError(PluginTest):
    __name__ = 'test-error'

    async def start(self):
        await asyncio.sleep(0.1, loop=self.loop)
        raise ValueError


@hookimpl
def plugins(loop):
    return PluginTestStartError(loop)
