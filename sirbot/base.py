from abc import ABC
from typing import Mapping


class Receiver(ABC):
    """ This is anything that can receive a message ie. a user, channel, etc.
    """
    pass


class User(Receiver):
    def __init__(self, user_id=None, channel_id=None):
        self._user_id = user_id
        self._channel_id = channel_id

    @property
    def id(self):
        return self._user_id


class Channel(Receiver):
    def __init__(self, channel_id):
        self._channel_id = channel_id

    @property
    def id(self):
        return self._channel_id


class Message:
    def __init__(self,
                 text: str='',
                 frm: Receiver=None,
                 to: Receiver=None,
                 data=Mapping,
                 history=None):
        self._text = text
        self._from = frm
        self._to = to
        self._data = data or {}

        if history:
            self.ctx = history.ctx
        else:
            self.ctx = {}

    def clone(self):
        return Message(self._text, self._from, self._to, self._data)

    @property
    def to(self) -> Receiver:
        return self._to

    @to.setter
    def to(self, to: Receiver):
        self._to = to

    @property
    def frm(self) -> Receiver:
        return self._from

    @frm.setter
    def frm(self, from_: Receiver):
        self._from = from_

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = text

    @property
    def history(self):
        return self._from

    def __str__(self):
        return self._text

    @property
    def is_direct_msg(self) -> bool:
        return isinstance(self.to, User)

    @property
    def is_channel_msg(self):
        return isinstance(self.to, Channel)
