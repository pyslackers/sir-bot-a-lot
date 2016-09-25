import logging

from .base import Serializer

logger = logging.getLogger('sirbot')


class Attachment(Serializer):
    def __init__(self, fallback, **kwargs):
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


class Action(Serializer):
    def __init__(self, name, text, type_, **kwargs):
        self.data = {'name': name, 'text': text, 'type': type_}
        self._add(**kwargs)

    def _add(self, **kwargs):
        for item, value in kwargs.items():
            self.data[item] = value

    def serialize(self):
        return self.data

    @property
    def text(self):
        return self.data['text']

    @text.setter
    def text(self, value):
        self.data['text'] = value

    @property
    def style(self):
        return self.data['style']

    @style.setter
    def style(self, value):
        self.data['style'] = value

    @property
    def value(self):
        return self.data['value']

    @value.setter
    def value(self, value):
        self.data['value'] = value

    @property
    def confirm(self):
        return self.data['confirm']

    @confirm.setter
    def confirm(self, value):
        self.data['confirm'] = value


class Button(Action):
    def __init__(self, name, text, **kwargs):
        super().__init__(name=name, text=text, type_='button', **kwargs)


class Field(Serializer):
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
        return self.data['value']

    @value.setter
    def value(self, value):
        self.data['value'] = value

    @property
    def short(self):
        return self.data['short']

    @short.setter
    def short(self, value):
        self.data['short'] = value

    @short.deleter
    def short(self):
        self.data.pop('short', None)

    def serialize(self):
        return self.data
