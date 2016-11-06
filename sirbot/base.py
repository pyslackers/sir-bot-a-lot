import json
import logging

from abc import ABC

logger = logging.getLogger('sirbot')


class MessageError(Exception):
    """Generic message error"""


class Receiver(ABC):
    """ This is anything that can receive a message ie. a user, channel, etc.
    """
    pass


class User(Receiver):
    """
    Class representing an user.
    """
    def __init__(self, user_id=None, channel_id=None):
        """
        :param user_id: id of the user
        """
        self._user_id = user_id
        self._channel_id = channel_id

    @property
    def id(self):
        return self._user_id

    @property
    def channel_id(self):
        return self._channel_id

    def __str__(self):
        return self.id


class Channel(Receiver):
    """
    Class representing a channel.
    """
    def __init__(self, channel_id, name, **kwargs):
        """
        :param channel_id: id of the channel
        :param name: name of the channel
        """
        self._channel_id = channel_id
        self._data = {'name': name}
        self.add(**kwargs)

    @property
    def id(self):
        return self._channel_id

    @property
    def channel_id(self):
        return self._channel_id

    @property
    def name(self):
        return self._data['name']

    @name.setter
    def name(self, name):
        self._data['name'] = name

    def get(self, *information):
        """
        Query information on the channel

        :param information: information needed
        :return: information
        :rtype: list
        """
        output_information = list()
        for info in information:
            output_information.append(self._data.get(info))
        return output_information

    def add(self, **kwargs):
        for item, value in kwargs.items():
            if item != 'id':
                self._data[item] = value

    def __str__(self):
        return self.id


class Serializer(ABC):
    def serialize(self):
        """
        Dump the content correctly formatted for the slack web API
        """


class Content(Serializer):
    """
    Content of a message.

    Independent of the channel/user.
    Can be use in multiple message.
    """
    def __init__(self, **kwargs):
        self.timestamp = None
        self.data = {'as_user': True,
                     'icon_emoji': ':robot_face:'}
        self.channel = None
        self.attachments = list()
        self._add(**kwargs)

    @property
    def text(self):
        return self.data['text']

    @text.setter
    def text(self, value):
        self.data['text'] = value

    def _add(self, **kwargs):
        for item, value in kwargs.items():
            self.data[item] = value

    def serialize(self):
        self.data['attachments'] = list()
        for attachment in self.attachments:
            self.data['attachments'].append(attachment.serialize())
        self.data['attachments'] = json.dumps(self.data['attachments'])
        return self.data


class Message(Serializer):
    """
    Class representing a message.
    """
    def __init__(self,
                 text: str='',
                 frm: Receiver=None,
                 to: Receiver=None,
                 history=None,
                 incoming=None,
                 timestamp=0,
                 content: Content = None):
        self._from = frm
        self._to = to
        self.timestamp = timestamp
        self.incoming = incoming
        self.content = content or Content()
        self.content.text = text
        self._reactions = None

        if history:
            self.ctx = history.ctx
        else:
            self.ctx = {}

    def clone(self, to: Receiver=None):
        """
        Clone the message

        :param to: Receiver of the new message
        :type to: Receiver
        :return: Clone of the original message
        :rtype: Message
        """
        return Message(frm=self._from,
                       to=to or self.to,
                       content=self.content)

    @property
    def to(self) -> Receiver:
        """
        Channel Receiver

        Channel where the message was posted
        or where it is going to be posted
        """
        return self._to

    @to.setter
    def to(self, to: Receiver):
        if isinstance(to, (User, Channel)):
            self._to = to

    @property
    def frm(self) -> Receiver:
        """
        User posting the message
        """
        return self._from

    @frm.setter
    def frm(self, from_: Receiver):
        self._from = from_

    @property
    def text(self) -> str:
        """
        Text of the Message

        Shortcut to access 'self.content.text'
        """
        return self.content.text

    @text.setter
    def text(self, text: str):
        self.content.text = text

    @property
    def attachments(self):
        """
        Attachments of the Message

        Shortcut to access 'self.content.attachments'
        """
        return self.content.attachments

    @property
    def history(self):
        return self._from

    @property
    def username(self) -> str:
        """
        Username used by the bot for this message if not default

        Shortcut to access 'self.content.data['username']'
        """
        return self.content.data['username']

    @username.setter
    def username(self, username: str):
        """
        Change the username of the bot for this message only.

        The as_user variable must be set to False.
        """
        self.content.data['as_user'] = False
        self.content.data['username'] = username

    @property
    def icon(self) -> str:
        """
        Icon used by the bot for this message if not default

        Shortcut to access 'self.content.data['icon_emoji']'
        or 'self.content.data['icon_url']'.
        If both value are set 'icon_emoji' is used first by the
        Slack API.
        """
        return self.content.data['icon_emoji'] or self.content.data['icon_url']

    @icon.setter
    def icon(self, icon: str):
        """
        Change the avatar of the bot for this message only.

        Change the bot avatar to an emoji or url to an image
        (See Slack API documentation for more information
        about the image size)
        The username attribute must be set for this to work.

        :param icon: emoji or url to use
        :type icon: str
        """
        if icon.startswith(':'):
            self.content.data['icon_emoji'] = icon
        else:
            self.content.data['icon_emoji'] = None
            self.content.data['icon_url'] = icon

    def __str__(self):
        return "<{} - {} - {} - {} - {}>".format(self.__class__.__name__,
                                                 self._to,
                                                 self._from,
                                                 self.timestamp,
                                                 self.content)

    @property
    def is_direct_msg(self) -> bool:
        return isinstance(self.to, User)

    @property
    def is_channel_msg(self):
        return isinstance(self.to, Channel)

    def serialize(self):
        data = self.content.serialize()
        if data.get('text') is False and data.get('attachments') is None:
            logger.warning('Message must have text or an attachments')
            raise MessageError('No text or attachments')
        data['channel'] = self.to.channel_id
        data['ts'] = self.timestamp
        return data
