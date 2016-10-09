import logging
import re
import asyncio
import functools

from aiohttp import web

from sirbot.base import Message, User, Channel
from .client import RTMClient, HTTPClient
from .channel import ChannelManager

logger = logging.getLogger('sirbot')


class SirBot:
    def __init__(self, token, *, loop: asyncio.AbstractEventLoop = None):
        self.loop = loop or asyncio.get_event_loop()
        self._rtm_client = RTMClient(token)
        self._http_client = HTTPClient(token)
        self.channels = ChannelManager(client=self._http_client)
        self.all_channels = ChannelManager(client=self._http_client)
        self.commands = {
            'listen': {}
        }
        self.event_handlers = {
            'message': self._message_handler,
            'channel': self._channel_handler,
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
                app.loop.create_task(self._get_channels())))

    @property
    def bot_id(self):
        return self._rtm_client._login_data['self']['id']

    @property
    def app(self):
        """Return the composed aiohttp application"""
        return self._app

    def listen(self, matchstr, flags=0, func=None):
        """
        DEPRECATED

        Decorator to register a plugin method. The plugin method will be called
        with a Message object and the message can be replied to with methods on
        the SirBot instance.

        This has been deprecated in favor of an upcoming plugin API (where the
        server will discover and use installed/available plugins).

        :param matchstr: The string (regex) to match in messages
        :param flags: Regex flags to use
        :param func: Function to call, note: this will be auto-resolved.
        :return: Original function, unmodified.
        """
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
        rtm_q = self._rtm_client.queue
        async for message in rtm_q:
            await self._dispatch_message(message)
            rtm_q.task_done()

    async def _dispatch_message(self, msg):
        """
        Dispatch the incoming slack message to the correct event handler.

        :param msg: incoming message
        """
        logger.debug('Dispatcher received message %s' % msg)
        subtype = msg.get('subtype', None)

        if subtype == 'message_changed':
            logger.debug('Ignoring changed message subtype')
            return
        elif subtype == 'message_deleted':
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

        if msg['type'].startswith('channel'):
            event_type = 'channel'
        else:
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
        """
        Handler for the incoming message of type 'message'

        Create a message object from the incoming message and sent it
        to the plugins

        :param msg: incoming message
        :return:
        """
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
            message.to = await self.channels.get(msg['channel'])

        await self._plugin_dispatcher(message)

    async def _channel_handler(self, msg):
        """
        Handler for the incoming message of type 'channel'

        Update both ChannelManager (bot channels and all channels) to keep an
        accurate inventory of the available channels.

        :param msg: Incoming message
        """
        logger.debug('Channel handler received %s', msg)

        msg_type = msg['type']
        try:
            channel_id = msg['channel'].get('id')
        except AttributeError:
            channel_id = msg['channel']

        if msg_type == 'channel_created':
            channel = Channel(channel_id=channel_id, **msg['channel'])
            self.all_channels.add(channel)
        elif msg_type == 'channel_deleted':
            self.all_channels.delete(channel_id)
            self.channels.delete(channel_id)
        elif msg_type == 'channel_joined':
            channel = self.all_channels.get(channel_id)
            self.channels.add(channel)
        elif msg_type == 'channel_left':
            self.channels.delete(channel_id)
        elif msg_type == 'channel_archive':
            self.all_channels.delete(channel_id)
            self.channels.delete(channel_id)
        elif msg_type == 'channel_unarchive':
            channel = Channel(channel_id=channel_id, name=channel_id)
            self.all_channels.add(channel)
            await self.all_channels.update(channel)
        elif msg_type == 'channel_rename':
            channel = await self.all_channels.get(channel_id)
            channel.name = msg['channel']['name']
        else:
            logger.debug('No channel event handler for this type %s, '
                         'ignoring ...' % msg_type)

    async def _plugin_dispatcher(self, msg):
        """
        Dispatch message to plugins
        """
        for matcher, func in self.commands['listen'].items():
            n = matcher.search(msg.text)
            if n:
                logger.debug('Located handler for text, invoking')
                rep = Message(to=msg.to, frm=msg.frm, incoming=msg)
                await func(rep, n.groups())

    async def send(self, *messages):
        """
        Send the messages provided and update their timestamp

        :param messages: Messages to send
        """
        for message in messages:
            message.timestamp = await self._http_client.send(
                message=message)

    async def update(self, *messages):
        """
        Update the messages provided and update their timestamp

        :param messages: Messages to update
        """
        for message in messages:
            message.timestamp = await self._http_client.update(
                message=message)

    async def delete(self, *messages):
        """
        Delete the messages provided

        :param messages: Messages to delete
        """
        for message in messages:
            message.timestamp = await self._http_client.delete(message)

    async def add_reaction(self, *messages):
        """
        Add a reaction to a message

        :Example:

        >>> bot.add_reaction([Message, 'thumbsup'], [Message, 'robotface'])
        Add the thumbup and robotface reaction to the message

        :param messages: List of message and reaction to add
        """
        for message, reaction in messages:
            await self._http_client.add_reaction(message, reaction)

    async def delete_reaction(self, *messages):
        """
        Delete reactions from messages

        :Example:

        >>> bot.delete_reaction([Message, 'thumbsup'], [Message, 'robotface'])
        Delete the thumbup and robotface reaction from the message

        :param messages: List of message and reaction to delete
        """
        for message, reaction in messages:
            await self._http_client.delete_reaction(message, reaction)

    async def get_reactions(self, *messages):
        """
        Query the reactions of messages

        :param messages: Messages to query reaction from
        :return: dictionary of reactions by message
        :rtype: dict
        """
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

    async def _get_channels(self):
        """
        Query all the channels of the team and update both ChannelManager

        Should be use only at startup. The channel handler keep both
        ChannelManager up to date afterwards by processing incoming channel
        event.
        """
        bot_channels, all_channels = await self._http_client.get_channels()
        self.channels.add(*bot_channels)
        self.all_channels.add(*all_channels)
        logger.info('Bot in channels: %s', self.channels.channels.keys())
        logger.info('All channels: %s', self.all_channels.channels.keys())

    def run(self, host: str = '0.0.0.0', port: int = 8080):
        web.run_app(self._app, host=host, port=port)
