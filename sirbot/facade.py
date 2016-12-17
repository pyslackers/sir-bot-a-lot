class MainFacade:
    """
    A class to compose all available functionality available to a bot
    or other plugin.

    Regroup all the facades of the plugins
    """
    def __init__(self, facades):
        self._facades = facades

    def get(self, plugin: str):
        """
        Search for the plugin facade and initialize it

        :param plugin: Facade to initialize
        :return: Plugin facade or None
        """
        facade = self._facades.get(plugin)
        if facade:
            return facade()
        return
