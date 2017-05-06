from .errors import FacadeNotAvailable


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
        :raise: FacadeNotAvailable
        """
        facade = self._facades.get(plugin)
        if facade:
            return facade()
        raise FacadeNotAvailable(plugin)

    def new(self):
        """
        Return a new instance of the MainFacade

        Should be called by plugins to have a new facade for each incoming
        message

        :return: MainFacade
        """
        return MainFacade(self._facades)

    def __len__(self):
        return len(self._facades)

    def __getitem__(self, item):
        return self._facades[item]()

    def __contains__(self, item):
        return item in self._facades
