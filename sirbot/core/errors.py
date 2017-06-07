class SirBotError(Exception):
    """
    Top level sirbot error
    """


class FacadeUnavailable(SirBotError):
    """
    The facade does not exist or the plugin has not started yet

    Args:
        facade: Name of the unavailable facade
    """
    def __init__(self, facade):

        #: Name of the unavailable facade
        self.facade = facade
