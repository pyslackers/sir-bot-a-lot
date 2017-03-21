from sirbot.hookimpl import hookimpl
from .sirbot import PluginTest


class PluginTestStartError(PluginTest):
    __name__ = 'test-error'

    async def start(self):
        raise ValueError


@hookimpl
def plugins(loop):
    return PluginTestStartError(loop)
