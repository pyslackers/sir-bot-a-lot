import logging

from .base import Serializer

logger = logging.getLogger('sirbot')


class Attachment(Serializer):
    """
    Class of a message attachment.

    An attachment can have multiple fields or actions. See
    Slack API documentation for more information about
    attachments.
    """
    def __init__(self, fallback, **kwargs):
        """
        :param fallback: String displayed if the client can not display
        attachments
        """
        self.data = {'mrkdwn_in': ["pretext", "text", "fields"],
                     'fallback': fallback}
        self.fields = list()
        self.actions = list()
        self._add(**kwargs)

    def _add(self, **kwargs):
        for item, value in kwargs.items():
            self.data[item] = value

    def serialize(self):
        self.data['fields'] = list()
        self.data['actions'] = list()
        for field in self.fields:
            self.data['fields'].append(field.serialize())
        for action in self.actions:
            self.data['actions'].append(action.serialize())
        return self.data


class _Action(Serializer):
    """
    Class representing an action in an Attachment.

    Only one type of action (Button) exist at the moment.
    See Slack API documentation for more information about
    actions.
    """
    def __init__(self, name, text, type_, **kwargs):
        """
        :param name: Name of the action. Sent to the callback url
        :param text: User facing text
        :param type_: Type of action. Only 'button' available
        """
        self.data = {'name': name, 'text': text, 'type': type_}
        self._add(**kwargs)

    def _add(self, **kwargs):
        for item, value in kwargs.items():
            self.data[item] = value

    def serialize(self):
        return self.data

    @property
    def text(self):
        """
        User facing label
        """
        return self.data['text']

    @text.setter
    def text(self, value):
        self.data['text'] = value

    @property
    def style(self):
        """
        Style of the action.

        Currently available: 'default', 'primary', 'danger'
        See Slack API documentation for more information
        """
        return self.data['style']

    @style.setter
    def style(self, value):
        self.data['style'] = value

    @property
    def value(self):
        """
        String identifying the specific action.

        Sent to the callback url alongside 'name' and 'callback_id'
        See Slack API documentation for more information
        """
        return self.data['value']

    @value.setter
    def value(self, value):
        self.data['value'] = value

    @property
    def confirm(self):
        """
        JSON used to display a confirmation message.

        See Slack API documentation for more information
        """
        return self.data['confirm']

    @confirm.setter
    def confirm(self, value):
        self.data['confirm'] = value


class Button(_Action):
    """
    Subclass of action representing a button.

    See Slack API documentation for more information.
    """
    def __init__(self, name, text, **kwargs):
        super().__init__(name=name, text=text, type_='button', **kwargs)


class Field(Serializer):
    """
    Class representing a field in an attachment.

    See slack API documentation for more information.
    """
    def __init__(self, **kwargs):
        self.data = dict()
        self._add(**kwargs)

    def _add(self, **kwargs):
        for item, value in kwargs.items():
            self.data[item] = value

    @property
    def title(self):
        return self.data['title']

    @title.setter
    def title(self, value):
        self.data['title'] = value

    @property
    def value(self):
        """
        Text/Value to show
        """
        return self.data['value']

    @value.setter
    def value(self, value):
        self.data['value'] = value

    @property
    def short(self):
        """
        Display fields side by side

        Specify if the fields is short enough to be displayed side by side
        in the Attachment.
        """
        return self.data['short']

    @short.setter
    def short(self, value):
        self.data['short'] = value

    @short.deleter
    def short(self):
        self.data.pop('short', None)

    def serialize(self):
        return self.data
