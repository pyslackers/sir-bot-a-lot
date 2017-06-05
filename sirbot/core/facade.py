from .errors import FacadeUnavailable


class MainFacade:
    """
    Class to compose all available facade.

    Args:
        facades (dict): Facade name and the associated factory
    """
    def __init__(self, facades):
        self._facades = facades

    def get(self, facade: str):
        """
        Search for the plugin facade and initialize it

        Args:
            facade (str): facade name

        Returns:
            Facade object return by :meth:`sirbot.core.plugin.Plugin.facade()`

        Raises:
            sirbot.core.errors.FacadeUnavailable: The facade does not exist or
             the plugin has not started yet

        """
        factory = self._facades.get(facade)
        if factory:
            return factory()
        raise FacadeUnavailable(facade)

    def new(self):
        """
        Return a new instance of the :class:`sirbot.core.facade.MainFacade`

        A new :class:`sirbot.core.facade.MainFacade`
        should be created for all incoming event.

        Returns:
            MainFacade: A new instance of
                :class:`sirbot.core.facade.MainFacade`
        """
        return MainFacade(self._facades)

    def __len__(self):
        return len(self._facades)

    def __getitem__(self, item):
        return self._facades[item]()

    def __contains__(self, item):
        return item in self._facades
