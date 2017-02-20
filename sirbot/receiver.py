import logging

logger = logging.getLogger('sirbot.core')


class Receiver:
    """
    This is anything that can receive a message ie. a user, channel, etc.

    send_id is the id where the message need to be sent to reach the receiver.
    """

    def __init__(self, id_, send_id=None):
        self.id = id_
        self.send_id = send_id or id_
