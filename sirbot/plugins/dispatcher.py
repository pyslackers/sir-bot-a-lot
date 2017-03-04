from abc import ABC


class Dispatcher(ABC):
    def __init__(self, loop):
        """
        Dispatcher for Sir-bot-a-lot

        :param loop: Event loop to work in, optional.
        """

    def configure(self, config):
        """
        Configure the plugin

        This method is called by the core after initialization

        :param config: configuration relevant to the slack plugin
        """

    async def incoming(self, msg, plugin_facade, facades):
        """
        Handle the incoming message

        This method is called for every incoming messages

        :param msg: incoming data
        :param plugin_facade: the plugin facade
        :param facades: all the available facades
        """

    def facade(self):
        """
        Initialize and return a new facade

        This is called by the core for each incoming message to this plugin
        and when another plugin request a facade
        """
