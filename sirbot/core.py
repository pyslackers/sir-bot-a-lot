import asyncio
import functools
import logging
import re
from typing import Optional

from aiohttp import web
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from sirbot.facade import BotFacade
from sirbot.base import Message, User, Channel
from sirbot.client import RTMClient, HTTPClient
from sirbot.channel import ChannelManager
from sirbot.queue import IterableQueue

logger = logging.getLogger('sirbot')


class SirBot:
    def __init__(self, token, *,
                 loop: Optional[asyncio.AbstractEventLoop] = None):
        self.loop = loop or asyncio.get_event_loop()

        # Named tasks, anything the bot is directly responsible for
        # maintaing the lifecycle of.
        self._tasks = {}

        self._rtm_client = RTMClient(token, loop=self.loop)
        self._rtm_queue = IterableQueue()
        self._http_client = HTTPClient(token, loop=self.loop)
        self._scheduler = AsyncIOScheduler()
        self._scheduler.start()

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

        self._app = web.Application(loop=self.loop)
        self._app.on_startup.append(self._start_background_tasks)
        self._app.on_cleanup.append(self._clean_background_tasks)

    async def _start_background_tasks(self, app: web.Application):
        """
        Start the background tasks
        :param app: aiohttp application instance.
        """
        self._tasks.update(
            rtm_connect=app.loop.create_task(
                self._rtm_client.connect(self._rtm_queue)),
            rtm_read=app.loop.create_task(self._rtm_read()),
            get_channels=app.loop.create_task(self._get_channels()),
        )

        # Ensure that if futures exit on error, they aren't silently ignored.
        def print_if_err(f):
            """Logs the error if one occurred causing the task to exit."""
            if f.exception() is not None:
                logger.error('Task exited with error: %s', f.exception())

        for task in self._tasks.values():
            task.add_done_callback(print_if_err)

    async def _clean_background_tasks(self, app):
        """
        Clean up the background tasks
        :param app: aiohttp application instance.
        """
        for task in self._tasks.values():
            task.cancel()
        await asyncio.gather(*self._tasks.values(), loop=self.loop)

    async def _rtm_read(self):
        """
        Read the from the message queue, most likely full of data
        from the Real Time Slack API.
        """
        try:
            rtm_q = self._rtm_queue
            async for message in rtm_q:
                await self._dispatch_message(message)
                rtm_q.task_done()
        except asyncio.CancelledError:
            pass

    async def _dispatch_message(self, msg):
        """
        Dispatch the incoming slack message to the correct event handler.

        :param msg: incoming message
        """
        logger.debug('Dispatcher received message %s', msg)
        msg_type = msg.get('type', None)
        ok = msg.get('ok', None)

        if msg_type.startswith('channel'):
            msg_type = 'channel'

        if msg_type == 'hello':
            logger.info('login data ok')
        elif ok:
            if msg.get('warning'):
                logger.info('API response: %s, %S', msg.get('warning'), msg)
            logger.debug('API response: %s', msg)
        elif ok is False:
            logger.info('API error: %s, %s', msg.get('error'), msg)
        elif msg_type is None:
            logging.debug('Ignoring non event message %s', msg)
            return
        else:
            logger.debug('Event Received: %s', msg)

        event_handler = self.event_handlers.get(msg_type)

        if event_handler is None:
            logger.debug('No event handler for this type %s, '
                         'ignoring ...', msg_type)
            return
        try:
            await event_handler(msg)
        except Exception:
            logger.exception('There was an issue with event handler %s',
                             event_handler)

    async def _message_handler(self, msg):
        """
        Handler for the incoming message of type 'message'

        Create a message object from the incoming message and sent it
        to the plugins

        :param msg: incoming message
        :return:
        """
        logger.debug('Message handler received %s', msg)
        ignoring = ['message_changed', 'message_deleted', 'channel_join',
                    'channel_leave']
        channel = msg.get('channel', None)

        if msg.get('subtype') in ignoring:
            logger.debug('Ignoring %s subtype', msg.get('subtype'))
            return
        else:
            logger.debug('Message Received: %s', msg)

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
            user = User(user, msg['channel'])
            message.frm = user
            message.to = user
        else:
            message.frm = User(user)
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
                         'ignoring ...', msg_type)

    async def _plugin_dispatcher(self, msg):
        """
        Dispatch message to plugins
        """
        for matcher, func in self.commands['listen'].items():
            n = matcher.search(msg.text)
            if n:
                logger.debug('Located handler for text, invoking')
                rep = Message(to=msg.to, frm=msg.frm, incoming=msg)
                await func(rep, n.groups(),
                           chat=BotFacade(self._http_client, self._scheduler))

    async def _get_channels(self):
        """
        Query all the channels of the team and update both ChannelManager

        Should be use only at startup. The channel handler keep both
        ChannelManager up to date afterwards by processing incoming channel
        event.
        """
        try:
            bot_channels, all_channels = await self._http_client.get_channels()
            self.channels.add(*bot_channels)
            self.all_channels.add(*all_channels)
            logger.info('Bot in channels: %s', self.channels.channels.keys())
            logger.info('All channels: %s', self.all_channels.channels.keys())
        except asyncio.CancelledError:
            pass

    @property
    def bot_id(self):
        return self._rtm_client.slack_id

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

    def run(self, host: str='0.0.0.0', port: int=8080):
        web.run_app(self._app, host=host, port=port)
