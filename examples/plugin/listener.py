import logging

from aiohttp.web import Response

from sirbot.core import Plugin, hookimpl

LOG = logging.getLogger(__name__)


@hookimpl
def plugins(loop):
    return ExampleListenerPlugin(loop)


class ExampleListenerPlugin(Plugin):

    __version__ = '0.0.1'
    __name__ = 'examplelistener'
    __facade__ = 'examplelistener'

    def __init__(self, loop):
        LOG.info('Initializing ExampleListenerPlugin')
        super().__init__(loop)
        self._loop = loop
        self._config = None
        self._router = None
        self._session = None
        self._facades = None
        self._endpoints = dict()

        self._started = False

    async def configure(self, config, router, session, facades):
        LOG.info('Configuring ExampleListenerPlugin')
        self._config = config
        self._router = router
        self._session = session
        self._facades = facades

        self._router.add_route('GET', '/{name}', self._incoming)

    async def start(self):
        LOG.info('Starting ExampleListenerPlugin')
        self._started = True

    async def update(self, config, plugins):
        pass

    @property
    def started(self):
        return self._started

    def facade(self):
        if not self.started:
            raise ValueError('pouet')
        LOG.info('Getting ExampleListenerPlugin facade')
        return ExampleListenerFacade(self._endpoints)

    async def _incoming(self, request):
        LOG.info('Incoming request')
        name = request.match_info['name']
        if name in self._endpoints:
            return await self._endpoints[name](request, self._facades.new())
        else:
            return Response(status=404, text='Not Found')


class ExampleListenerFacade:

    def __init__(self, endpoints):
        self._endpoints = endpoints

    def add(self, name, func):
        LOG.info('Adding endpoint %s to ExampleListenerPlugin', name)
        self._endpoints[name] = func
