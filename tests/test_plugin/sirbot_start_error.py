from sirbot.hookimpl import hookimpl
from .sirbot import PluginTest


class PluginTestStartError(PluginTest):
    async def start(self):
        raise ValueError


@hookimpl
def plugins(loop):
    return 'test', PluginTestStartError(loop)
