class Content:
    """
    Content of a message.

    Independent of the from/to.
    Can be use in multiple message.
    """
    def __init__(self, **kwargs):
        self.data = dict()
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


class Message:
    """
    Class representing a message.
    """

    def __init__(self,
                 text='',
                 frm=None,
                 to=None,
                 incoming=None,
                 content=Content,
                 timestamp=0):

        self.frm = frm
        self.to = to

        self.content = content()
        self.content.text = text

        self.incoming = incoming
        self.timestamp = timestamp

    # def clone(self, to: Receiver=None):
    #     """
    #     Clone the message
    #
    #     :param to: Receiver of the new message
    #     :type to: Receiver
    #     :return: Clone of the original message
    #     :rtype: Message
    #     """
    #     return Message(frm=self._from,
    #                    to=to or self.to,
    #                    content=self.content)

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

    def response(self):
        """
        Create a new message with the same destination `to`
        and the current message as incoming

        :return Message
        """
        return Message(to=self.to,
                       incoming=self)
