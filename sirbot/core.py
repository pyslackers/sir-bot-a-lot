import asyncio
import logging
import functools
import pluggy
import importlib

from typing import Optional
from aiohttp import web

from . import hookspecs
from .facade import MainFacade

logger = logging.getLogger('sirbot.core')


class SirBot:
    def __init__(self, config=None, *,
                 loop: Optional[asyncio.AbstractEventLoop] = None):

        self.config = config or {}
        self._configure()
        logger.info('Initializing Sir-bot-a-lot')

        self.loop = loop or asyncio.get_event_loop()
        self._tasks = {}
        self._dispatcher = None
        self._pm = None
        self._plugins = dict()
        self._facades = dict()

        self._import_plugins()
        self._app = web.Application(loop=self.loop,
                                    middlewares=(self._middleware_factory,))
        self._app.on_startup.append(functools.partial(self._start))
        self._app.on_cleanup.append(self._clean_background_tasks)

        self._initialize_plugins()
        self._registering_facades()
        self._configuring_plugins()
        logger.info('Sir-bot-a-lot Initialized')

    def _configure(self) -> None:
        """
        Configure Sirbot

=       :return: None
        """

        if 'loglevel' in self.config.get('core', {}):
            logger.setLevel(self.config['core']['loglevel'])
        if 'loglevel' in self.config:
            logging.getLogger('sirbot').setLevel(self.config['loglevel'])

    async def _start(self, app: web.Application) -> None:
        """
        Startup tasks
        """
        logger.info('Starting Sir-bot-a-lot ...')

        await self._start_plugins()

        # Ensure that if futures exit on error, they aren't silently ignored.
        def print_if_err(f):
            """Logs the error if one occurred causing the task to exit."""
            if f.exception() is not None:
                logger.error('Task exited with error: %s', f.exception())

        for task in self._tasks.values():
            task.add_done_callback(print_if_err)

        logger.info('Sir-bot-a-lot started !')

    def _initialize_plugins(self) -> None:
        """
        Initialize and start the plugins
        """
        logger.debug('Initializing plugins')
        plugins = self._pm.hook.plugins(loop=self.loop)
        if plugins:
            for plugin in plugins:
                self._plugins[plugin[0]] = plugin[1]
        else:
            logger.error('No plugins found')

    def _registering_facades(self) -> None:

        for name, plugin in self._plugins.items():
            plugin_facade = getattr(plugin, 'facade', None)
            if callable(plugin_facade):
                self._facades[name] = plugin.facade

    def _configuring_plugins(self) -> None:

        for name, plugin in self._plugins.items():
            plugin.configure(self.config.get(name, {}),
                             self._app.router,
                             MainFacade(self._facades))

    async def _start_plugins(self) -> None:
        logger.debug('Starting plugins')
        for name, plugin in self._plugins.items():
            self._tasks[name] = self.loop.create_task(plugin.start())

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

    async def _middleware_factory(self, app, handler):
        async def middleware_handler(request):
            request['facades'] = MainFacade(self._facades)
            return await handler(request)
        return middleware_handler

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
        web.run_app(self._app, host=host, port=port)  # pragma: no cover
