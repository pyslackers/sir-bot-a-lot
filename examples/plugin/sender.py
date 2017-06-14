import logging

from sirbot.core import Plugin, hookimpl


LOG = logging.getLogger(__name__)


@hookimpl
def plugins(loop):
    return ExampleSenderPlugin(loop)


class ExampleSenderPlugin(Plugin):

    __version__ = '0.0.1'
    __name__ = 'examplesender'
    __facade__ = 'examplesender'

    def __init__(self, loop):
        LOG.info('Initializing ExampleSenderPlugin')
        super().__init__(loop)
        self._loop = loop
        self._config = None
        self._router = None
        self._session = None
        self._facades = None
        self._started = False

    async def configure(self, config, router, session, facades):
        LOG.info('Configuring ExampleSenderPlugin')
        self._config = config
        self._router = router
        self._session = session
        self._facades = facades

    async def start(self):
        LOG.info('Starting ExampleSenderPlugin')
        self._started = True

    async def update(self, config, plugins):
        pass

    @property
    def started(self):
        return self._started

    def facade(self):
        LOG.info('Getting ExampleSenderPlugin facade')
        return ExampleSenderPluginFacade(self._session)


class ExampleSenderPluginFacade:

    def __init__(self, session):
        self.session = session

    async def get(self, url):
        LOG.info('Fetching url: %s', url)
        return await self.session.get(url)
