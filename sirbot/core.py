import logging
import re
import asyncio
import functools

from aiohttp import web

from sirbot.base import Message, User
from .client import RTMClient, HTTPClient

logger = logging.getLogger('sirbot')


class SirBot:
    def __init__(self, token, *, loop: asyncio.AbstractEventLoop = None):
        self.loop = loop or asyncio.get_event_loop()
        self._rtm_client = RTMClient(token)
        self._http_client = HTTPClient(token)
        self.channels = None
        self.all_channels = None
        self.commands = {
            'listen': {}
        }
        self.event_handlers = {
            'message': self._message_handler,
            'channel_created': self._created_channel_handler,
        }
        self.mentioned_regex = re.compile(
            r'^(?:\<@(?P<atuser>\w+)\>:?|(?P<username>\w+)) ?(?P<text>.*)$')

        self._app = web.Application(loop=loop)
        self._app['tasks'] = []
        self._app.on_startup.append(
            lambda app: app['tasks'].append(
                app.loop.create_task(self._rtm_client.rtm_connect())))
        self._app.on_startup.append(
            lambda app: app['tasks'].append(
                app.loop.create_task(self.rtm_read())))
        self._app.on_startup.append(
            lambda app: app['tasks'].append(
                app.loop.create_task(self.get_channel())))

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
        self.commands['listen'][re.compile(matchstr, flags)] = wrapped

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
        elif subtype == u'message_deleted':
            logger.debug('Ignoring deleted message subtype')
            return
        elif subtype == 'channel_join':
            logger.debug('Ignoring channel join message')
            return
        elif subtype == 'channel_leave':
            logger.debug('Ignoring channel join message')
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
            timestamp = msg['message']['ts']
        else:
            text = msg['text']
            user = msg.get('user', msg.get('bot_id'))
            timestamp = msg['ts']

        message = Message(text=text, timestamp=timestamp)

        if channel.startswith('D'):
            # If the channel starts with D it is a direct message to the bot
            message.frm = User(user, msg['channel'])
            message.to = User(msg['channel'])
        else:
            message.frm = User(user, msg['channel'])
            message.to = self.channels.get(msg['channel'])
            if message.to is None:
                raise Exception

        await self._plugin_dispatcher(message)

    async def _created_channel_handler(self, msg):
        logger.debug('Channel created handler received {}'.format(msg))

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

    async def delete(self, *messages):
        for message in messages:
            message.timestamp = await self._http_client.delete(message)

    async def add_reaction(self, *messages):
        for message, reaction in messages:
            await self._http_client.add_reaction(message, reaction)

    async def delete_reaction(self, *messages):
        for message, reaction in messages:
            await self._http_client.delete_reaction(message, reaction)

    async def get_reactions(self, *messages):
        reactions = dict()
        for message in messages:
            msg_reactions = await self._http_client.get_reaction(message)
            for msg_reaction in msg_reactions:
                users = list()
                for user_id in msg_reaction.get('users'):
                    users.append(User(user_id=user_id))
                msg_reaction['users'] = users
            reactions[message] = msg_reactions
            message.reactions = msg_reactions
        return reactions

    async def get_channel(self):
        logger.debug('Getting channels')
        self.channels, self.all_channels = \
            await self._http_client.get_channels()
        logger.info('Available channels: {}'.format(self.channels))

    def run(self, host: str='0.0.0.0', port: int=8080):
        web.run_app(self._app, host=host, port=port)
