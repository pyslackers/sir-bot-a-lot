import logging
import re
import asyncio
import functools

from sirbot.base import Message, User, Channel
from .client import RTMClient, HTTPClient

logger = logging.getLogger('sirbot')


class SirBot:
    def __init__(self, token, *, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self._rtm_client = RTMClient(token)
        self._http_client = HTTPClient(token)
        self.commands = {
            'listen': {}
        }
        self.event_handlers = {
            'message': self._message_handler
        }
        self.mentioned_regex = re.compile(
            r'^(?:\<@(?P<atuser>\w+)\>:?|(?P<username>\w+)) ?(?P<text>.*)$')

        # These are for future purposes. HTTPClient is to send messages via
        # the http api.
        # The webserver is to allow for webhooks and/or web frontend.
        # This will probably be built with aiohttp.

        # self._http_client = HTTPClient(token)
        # self._web_server = WebServer()

    @property
    def bot_id(self):
        return self._rtm_client._login_data['self']['id']

    def listen(self, matchstr, flags=0, func=None):
        if func is None:
            logger.debug('No function provided, providing a partial.')
            return functools.partial(self.listen, matchstr, flags)
        wrapped = func

        if not asyncio.iscoroutinefunction(wrapped):
            logger.debug('Function is not a coroutine, converting.')
            wrapped = asyncio.coroutine(wrapped)
        logger.debug('Registering listener for "%s"', matchstr)
        self.commands['listen'][re.compile(matchstr, flags)] = func

        # Return original func
        return func

    async def rtm_read(self):

        while True:
            msg = await self._rtm_client.queue.get()

            await self._dispatch_message(msg)

    async def _dispatch_message(self, msg):
        """
         Process handler for incoming slack messages
        :param msg:
        :return:
        """
        logger.debug('Dispatcher received message %s' % msg)

        subtype = msg.get('subtype', None)

        if subtype == u'message_changed':
            logger.debug('Ignoring changed message subtype')
            return

        if subtype == u'message_deleted':
            logger.debug('Ignoring deleted message subtype')
            return

        if 'type' not in msg:
            logging.debug('Ignoring non event message %s' % msg)
            return

        event_type = msg['type']

        event_handler = self.event_handlers.get(event_type)

        if event_handler is None:
            logger.debug('No event handler for this type %s, '
                         'ignoring ...' % event_type)
            return

        try:
            await event_handler(msg)
        except Exception:
            logger.exception('There was an issue with event handler %s'
                             % event_handler)

    async def _message_handler(self, msg):
        logger.debug('Message handler received %s' % msg)

        channel = msg.get('channel', None)

        if channel[0] not in 'CGD':
            logger.debug('Unknown channel, Unable to handle this channel: %s',
                         channel)
            return

        if 'message' in msg:
            text = msg['message']['text']
            user = msg['message'].get('user', msg.get('bot_id'))
        else:
            text = msg['text']
            user = msg.get('user', msg.get('bot_id'))

        message = Message(text)

        if channel.startswith('D'):
            # If the channel starts with D it is a direct message to the bot
            message.frm = User(user, msg['channel'])
            message.to = User(msg['channel'])
        else:
            message.frm = User(user, msg['channel'])
            message.to = Channel(msg['channel'])

        await self._plugin_dispatcher(message)

    async def _plugin_dispatcher(self, msg):

        for matcher, func in self.commands['listen'].items():
            n = matcher.search(msg.text)
            if n:
                logger.debug('Located handler for text, invoking')
                rep = Message(to=msg.to, frm=msg.frm, incoming=msg)
                await func(rep, n.groups())

    async def send(self, *messages):
        for message in messages:
            message.timestamp = await self._http_client.send(
                message=message, method="send")

    async def update(self, *messages):
        for message in messages:
            message.timestamp = await self._http_client.send(
                message=message, method='update')

    def run(self):
        tasks = [
            self.loop.create_task(self._rtm_client.rtm_connect()),
            self.loop.create_task(self.rtm_read())
        ]
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            for task in tasks:
                task.cancel()
            self.loop.close()
