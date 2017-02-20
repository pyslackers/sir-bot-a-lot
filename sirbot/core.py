import asyncio
import logging
import functools
import pluggy
import importlib
import yaml

from typing import Optional
from aiohttp import web

from sirbot.iterable_queue import IterableQueue
from sirbot.dispatcher import Dispatcher
from sirbot import hookspecs

logger = logging.getLogger('sirbot.core')


class SirBot:
    def __init__(self, config_file=None, *,
                 loop: Optional[asyncio.AbstractEventLoop] = None):

        self.loop = loop or asyncio.get_event_loop()
        self._tasks = {}
        self._dispatcher = None
        self._pm = None

        if config_file:
            self.config = self.load_config(config_file)
        else:
            self.config = dict()

        self._clients = dict()

        self._app = web.Application(loop=self.loop)
        self._app.on_startup.append(functools.partial(self._start))
        self._app.on_cleanup.append(self._clean_background_tasks)

    def load_config(self, config_file: str) -> dict:
        """
        Load the configuration from a yaml file and set the core log level

        :param config_file: path of the file
        :return: configuration
        """
        with open(config_file) as file:
            self.config = yaml.load(file)

        if 'loglevel' in self.config['core']:
            logger.setLevel(self.config['core']['loglevel'])
        if 'loglevel' in self.config:
            logging.getLogger('sirbot').setLevel(self.config['loglevel'])

        return self.config

    async def _start(self, app: web.Application) -> None:
        logger.info('Starting Sir-bot-a-lot ...')
        self._import_plugins()

        self._incoming_queue = IterableQueue(loop=self.loop)
        self._dispatcher = Dispatcher(self._pm, self.config, self.loop)

        await self._initialize_clients()

        self._tasks['incoming'] = self.loop.create_task(
            self._read_incoming_queue())

        # Ensure that if futures exit on error, they aren't silently ignored.
        def print_if_err(f):
            """Logs the error if one occurred causing the task to exit."""
            if f.exception() is not None:
                logger.error('Task exited with error: %s', f.exception())

        for task in self._tasks.values():
            task.add_done_callback(print_if_err)

        logger.info('Sir-bot-a-lot started !')

    async def _initialize_clients(self) -> None:
        """
        Initialize and start the clients
        """
        logger.debug('Initializing clients')
        clients = self._pm.hook.clients(loop=self.loop,
                                        config=self.config,
                                        queue=self._incoming_queue)
        if clients:
            for client in clients:
                self._clients[client[0]] = client[1]
                self._tasks[client[0]] = self.loop.create_task(
                    client[1].connect())
        else:
            logger.error('No client found')

    def _import_plugins(self) -> None:
        """
        Import and register the plugins

        Most likely composed of a client and a dispatcher
        """
        logger.debug('Importing plugins')
        self._pm = pluggy.PluginManager('sirbot')
        self._pm.add_hookspecs(hookspecs)

        if 'core' in self.config and 'plugins' in self.config['core']:
            for plugin in self.config['core']['plugins']:
                p = importlib.import_module(plugin)
                self._pm.register(p)

    async def _clean_background_tasks(self, app) -> None:
        """
        Clean up the background tasks
        """
        for task in self._tasks.values():
            task.cancel()
        await asyncio.gather(*self._tasks.values(), loop=self.loop)

    async def _read_incoming_queue(self) -> None:
        """
        Read from the incoming message queue
        """
        try:
            async for message in self._incoming_queue:
                logger.debug('Incoming message received from %s',
                             message[0])
                await self._dispatcher.incoming_message(message[0], message[1])
                self._incoming_queue.task_done()
        except asyncio.CancelledError:
            pass

    @property
    def app(self) -> web.Application:
        """
        Return the composed aiohttp application
        """
        return self._app

    def run(self, host: str = '0.0.0.0', port: int = 8080):
        """
        Start the bot
        """
        web.run_app(self._app, host=host, port=port)
