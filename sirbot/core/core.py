"""
sirbot core

Core API of Sir-bot-a-lot
"""

import asyncio
import importlib
import logging
import logging.config
import os
import aiohttp
import pluggy
import yaml

from collections import defaultdict
from aiohttp import web

from sirbot.utils import merge_dict

from . import hookspecs
from .facade import MainFacade

logger = logging.getLogger(__name__)


class SirBot:
    """
    Initialize sirbot and load plugins. Core and logging configuration is
    done on initialization. Plugins configuration is done on startup.

    Args:
        config (dict): Configuration of Sir-bot-a-lot
        loop (asyncio.AbstractEventLoop): Event loop
    """
    def __init__(self, config=None, *, loop=None):
        self.config = config or {}
        self._configure()
        logger.info('Initializing Sir-bot-a-lot')

        self._loop = loop or asyncio.get_event_loop()
        self._tasks = {}
        self._dispatcher = None
        self._pm = None
        self._session = aiohttp.ClientSession(loop=self._loop)
        self._plugins = dict()

        self._start_priority = defaultdict(list)
        self._facades = dict()

        self._import_plugins()
        self._app = web.Application(loop=self._loop)
        self._app.on_startup.append(self._start)
        self._app.on_cleanup.append(self._stop)

        self._initialize_plugins()
        self._registering_facades()

        logger.info('Sir-bot-a-lot Initialized')

    def _configure(self):
        """
        Configure the core of sirbot

        Merge the config with the default core config and configure logging.
        The default logging level is `INFO`
        """
        path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'config.yml'
        )

        with open(path) as file:
            defaultconfig = yaml.load(file)

        self.config = merge_dict(self.config, defaultconfig)

        if 'logging' in self.config:
            logging.config.dictConfig(self.config['logging'])
        else:
            logging.getLogger('sirbot').setLevel('INFO')

    async def _start(self, app: web.Application) -> None:
        """
        Start sirbot
        """
        logger.info('Starting Sir-bot-a-lot ...')
        await self._start_plugins()

        logger.info('Sir-bot-a-lot fully started')

    async def _stop(self, app) -> None:
        """
        Stop sirbot
        """
        logger.info('Stopping Sir-bot-a-lot ...')

        for task in self._tasks.values():
            task.cancel()
        await asyncio.gather(*self._tasks.values(), loop=self._loop)
        await self._session.close()

        logger.info('Sir-bot-a-lot fully stopped')

    def _import_plugins(self) -> None:
        """
        Import and register plugin in the plugin manager.

        The pluggy library is used as plugin manager.
        """
        logger.debug('Importing plugins')
        self._pm = pluggy.PluginManager('sirbot')
        self._pm.add_hookspecs(hookspecs)

        for plugin in self.config['sirbot']['plugins']:
            p = importlib.import_module(plugin)
            self._pm.register(p)

    def _initialize_plugins(self):
        """
        Initialize the plugins

        Query the configuration and the plugins for info
        (name, facade name, start priority, etc)
        """
        logger.debug('Initializing plugins')
        plugins = self._pm.hook.plugins(loop=self._loop)
        if plugins:
            for plugin in plugins:
                name = plugin.__name__
                facade = plugin.__facade__ or plugin.__name__
                config = self.config.get(name, {})

                priority = config.get('priority', 50)

                if priority:
                    self._plugins[name] = {
                        'plugin': plugin,
                        'config': config,
                        'priority': priority,
                        'facade': facade
                    }

                    self._start_priority[priority].append(name)
        else:
            logger.error('No plugins found')

    def _registering_facades(self):
        """
        Index the available facades

        Query the plugins for an usable facade and register it
        """
        for name, info in self._plugins.items():
            if info['priority']:
                plugin_facade = getattr(info['plugin'], 'facade', None)
                if callable(plugin_facade):
                    self._facades[info['facade']] = info['plugin'].facade

    async def _configure_plugins(self) -> None:
        """
        Configure the plugins

        Asynchronously configure the plugins.
        Each plugins get a MainFacade object to check the available facades.
        Facade can not be loaded as the bot hasn't started yet.
        """
        logger.debug('Configuring plugins')
        funcs = [
            info['plugin'].configure(
                config=info['config'],
                session=self._session,
                facades=MainFacade(self._facades),
                router=self.app.router
            )
            for info in self._plugins.values()
        ]

        if funcs:
            await asyncio.gather(*funcs, loop=self._loop)
        logger.debug('Plugins configured')

    async def _start_plugins(self) -> None:
        """
        Start the plugins by priority

        Start the plugins based on the priority and wait for them to be fully
        started before starting the next one. This ensure that the facade of
        previously started plugin is usable.
        """
        logger.debug('Starting plugins')
        for priority in sorted(self._start_priority, reverse=True):
            logger.debug(
                'Starting plugins %s',
                ', '.join(self._start_priority[priority])
            )

            for name in self._start_priority[priority]:
                plugin = self._plugins[name]
                self._tasks[name] = self._loop.create_task(
                    plugin['plugin'].start()
                )

            while not all(self._plugins[name]['plugin'].started
                          for name in self._tasks):

                for task in self._tasks.values():
                    if task.done():
                        task.result()
                await asyncio.sleep(0.2, loop=self._loop)

            else:
                logger.debug('Plugins %s started',
                             ', '.join(self._start_priority[priority]))

    async def update(self):
        """
        Update sirbot

        Trigger the update method of the plugins. This is needed if the plugins
        need to perform update migration (i.e database)
        """
        for name, plugin in self._plugins.items():
            plugin_update = getattr(plugin['plugin'], 'update', None)
            if callable(plugin_update):
                logger.info('Updating %s', name)
                await plugin_update(self.config.get(name, {}), self._plugins)
                logger.info('%s updated', name)
        self._session.close()

    @property
    def app(self) -> web.Application:
        """

        Returns: The composed aiohttp.web.Application

        """
        return self._app

    def run(self, host: str = '0.0.0.0', port: int = 8080):
        """
        Start sirbot

        Configure sirbot and start the aiohttp.web.Application

        Args:
            host (str): host
            port (int): port
        """
        self._loop.run_until_complete(self._configure_plugins())
        web.run_app(self._app, host=host, port=port)  # pragma: no cover
