from sirbot.core.errors import SirBotALotError, MessageError


def test_errors():
    assert issubclass(MessageError, SirBotALotError)
