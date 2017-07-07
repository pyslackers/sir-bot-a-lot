from abc import ABC


class Plugin(ABC):  # pragma: no cover
    """
    Plugin for sirbot

    The loop should be explicitly passed in the plugin

    Args:
        loop (asyncio.AbstractEventLoop): Event loop
    """

    __version__ = '0.0.1'
    """Current version of the plugin"""

    __name__ = 'plugin'
    """Name of the plugin"""

    __registry__ = ''
    """Name in the registry. Default to the plugin name."""

    def __init__(self, loop):
        pass

    async def configure(self, config, router, session, registry):
        """
        Method called after the initialization of all plugins

        Args:
            config (dict): configuration for this plugin
            router (aiohttp.web_urldispatcher.UrlDispatcher): incoming request
                router
            session (aiohttp.ClientSession): Session
            registry (sirbot.core.registry.Registry): registry of all available
                plugins factories
        """
        pass

    async def start(self):
        """
        Method called at the bot startup

        Plugins with a higher priority will be started first

        Stored as an asyncio tasks. Is kept running while the bot is alive.
        All incoming data (if any) should be processed here.
        """
        pass

    async def update(self, config, plugins):
        """
        Method called by :meth:`sirbot.core.SirBot.update`

        Perform any update to the plugin configuration here.

        Args:
            config (dict): configuration for this plugin
            plugins (dict[name, plugin]): initialized plugins
        """
        pass

    @property
    def started(self):
        """
        Plugins successfully started

        This property should be set as :code:`True`
        when the plugin is fully started.
        """
        return False

    def factory(self):
        """
        Plugin factory

        Called when requesting this plugin from the registry. Interaction point
        between the plugins.
        """
        return
