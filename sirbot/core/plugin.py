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

    __facade__ = ''
    """Name of the facade"""

    def __init__(self, loop):
        pass

    async def configure(self, config, router, session, facades):
        """
        Method called after the initialization of all plugins

        Args:
            config (dict): configuration for this plugin
            router (aiohttp.web_urldispatcher.UrlDispatcher): incoming request
                router
            session (aiohttp.ClientSession): Session
            facades (sirbot.core.facade.MainFacade): facades of all available
                plugins
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

    def facade(self):
        """
        Facade factory

        Used by the :meth:`sirbot.core.facade.MainFacade.get` method
        """
        return False
