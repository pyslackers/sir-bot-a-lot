from abc import ABC


class Plugin(ABC):  # pragma: no cover
    __version__ = '0.0.1'
    __name__ = 'test'

    def __init__(self, loop):
        """
        Method called at the bot initialization.


        Nothing big should be executed by a plugin at this point.
        Please explicitly pass the loop in the plugin.

        :param loop: asyncio loop
        """

    async def configure(self, config, router, session, facades):
        """
        Method called after the initialization of all plugins



        :param config: configuration for this plugin
        :param router: aiohttp UrlDispatcher
        :param session: aiohttp client session
        :param facades: facades of all available plugins
        :return: None
        """
        pass

    async def start(self):
        """
        Method called at the bot startup

        Stored as an asyncio tasks. Is kept running while the bot is alive.
        All incoming data (if any) should be processed here.

        :return: None
        """
        pass

    @property
    def started(self):
        """
        Plugins successfully started

        This property should be set as True when the plugin is fully started.
        """
        return False

    # def facade(self):
    #     """
    #     OPTIONAL Method called when a plugin request the facade of this
    #     plugin
    #
    #     Should return a class for interacting with the service API
    #
    #     :return: None
    #     """
