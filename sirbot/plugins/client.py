from abc import ABC


class Client(ABC):
    def __init__(self, loop, queue):
        """
        Client for Sir-bot-a-lot.

        :param loop: Event loop to work in, optional.
        :param queue: Incoming data queue
        """

    def configure(self, config, router):
        """
        Configure the client

        This method is called by the core after the initialization of
        the client

        :param config: configuration relevant to the plugin
        :param router: aiohttp router
        :return: None
        """

    async def connect(self):
        """
        Connect the client

        This method is called by the core at startup of the bot and stored as
        an asyncio tasks.
        The client should dump data into the incoming queue here.
        """
