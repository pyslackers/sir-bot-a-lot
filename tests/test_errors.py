from sirbot.errors import SirBotALotError, MessageError


def test_errors():
    assert issubclass(MessageError, SirBotALotError)
