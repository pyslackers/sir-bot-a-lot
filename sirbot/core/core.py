"""
sirbot core

Core API of Sir Bot-a-lot
"""

import asyncio
import importlib
import logging
import logging.config
import os
import sys
import aiohttp
import pluggy
import yaml

from collections import defaultdict
from aiohttp import web

from sirbot.utils import merge_dict

from . import hookspecs
from .registry import Registry

logger = logging.getLogger(__name__)

if sys.version_info[:2] == (3, 5):
    ModuleNotFoundError = ImportError


class SirBot:
    """
    Initialize sirbot and load plugins. Core and logging configuration is
    done on initialization. Plugins configuration is done on startup.

    Args:
        config (dict): Configuration of Sir Bot-a-lot
        loop (asyncio.AbstractEventLoop): Event loop
    """
    def __init__(self, config=None, *, loop=None):
        self.config = config or {}
        self._configure()
        logger.info('Initializing Sir Bot-a-lot')

        self._loop = loop or asyncio.get_event_loop()
        self._tasks = {}
        self._dispatcher = None
        self._pm = None
        self._plugins = dict()

        self._start_priority = defaultdict(list)
        self._registry = Registry()

        self._import_plugins()
        self._app = web.Application(loop=self._loop)
        self._app.on_startup.append(self._start)
        self._app.on_cleanup.append(self._stop)

        self._initialize_plugins()
        self._register_factory()
        self._session = aiohttp.ClientSession(loop=self._loop)

        logger.info('Sir Bot-a-lot Initialized')

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
        logger.info('Starting Sir Bot-a-lot ...')
        await self._start_plugins()

        logger.info('Sir Bot-a-lot fully started')

    async def _stop(self, app) -> None:
        """
        Stop sirbot
        """
        logger.info('Stopping Sir Bot-a-lot ...')

        for task in self._tasks.values():
            task.cancel()
        await asyncio.gather(*self._tasks.values(), loop=self._loop)
        await self._session.close()

        logger.info('Sir Bot-a-lot fully stopped')

    def _import_plugins(self) -> None:
        """
        Import and register plugin in the plugin manager.

        The pluggy library is used as plugin manager.
        """
        logger.debug('Importing plugins')
        self._pm = pluggy.PluginManager('sirbot')
        self._pm.add_hookspecs(hookspecs)

        for plugin in self.config['sirbot']['plugins']:
            try:
                p = importlib.import_module(plugin)
            except (ModuleNotFoundError, ):
                if os.getcwd() not in sys.path:
                    sys.path.append(os.getcwd())
                    p = importlib.import_module(plugin)
                else:
                    raise
            self._pm.register(p)

    def _initialize_plugins(self):
        """
        Initialize the plugins

        Query the configuration and the plugins for info
        (name, registry name, start priority, etc)
        """
        logger.debug('Initializing plugins')
        plugins = self._pm.hook.plugins(loop=self._loop)
        if plugins:
            for plugin in plugins:
                name = plugin.__name__
                registry_name = plugin.__registry__ or plugin.__name__
                config = self.config.get(name, {})

                priority = config.get('priority', 50)

                if priority:
                    self._plugins[name] = {
                        'plugin': plugin,
                        'config': config,
                        'priority': priority,
                        'factory': registry_name
                    }

                    self._start_priority[priority].append(name)
        else:
            logger.error('No plugins found')

    def _register_factory(self):
        """
        Index the available factories

        Query the plugins for an usable factory and register it
        """
        for name, info in self._plugins.items():
            if info['priority']:
                factory = getattr(info['plugin'], 'factory', None)
                if callable(factory):
                    self._registry[info['factory']] = info['plugin'].factory
        self._registry.freeze()

    async def _configure_plugins(self) -> None:
        """
        Configure the plugins

        Asynchronously configure the plugins. Pass them their configuration,
        the aiohttp session, the registry and the aiohttp router
        """
        logger.debug('Configuring plugins')
        funcs = [
            info['plugin'].configure(
                config=info['config'],
                session=self._session,
                registry=self._registry,
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
        started before starting the next one. This ensure plugins can use
        a previously started one during startup.
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
