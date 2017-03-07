class SirBotALotError(Exception):
    """
    Generic Sir-bot-a-lot error
    """


class MessageError(SirBotALotError):
    """
    Generic message error
    """


class FacadeNotAvailable(SirBotALotError):
    """
    Error when the requested facade is not available
    """

    def __init__(self, facade=''):
        self.facade = facade
