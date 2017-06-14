import logging

from sirbot.core import Plugin, hookimpl
from aiohttp.web import Response

LOG = logging.getLogger(__name__)


@hookimpl
def plugins(loop):
    """
    Hook to register the plugin in Sir-bot-a-lot

    Args:
        loop (asyncio.AbstractEventLoop): Event loop

    Returns: An instance of `ExampleConfigPlugin`

    """
    return ExampleConfigPlugin(loop)


class ExampleConfigPlugin(Plugin):
    """
    Example configuration plugin for Sir-bot-a-lot.


    """

    __version__ = '0.0.1'
    __name__ = 'exampleconfig'
    __facade__ = 'exampleconfig'

    def __init__(self, loop):

        super().__init__(loop)
        LOG.info('Initializing ExampleConfigPlugin')
        self._loop = loop
        self._config = None
        self._router = None
        self._session = None
        self._facades = None
        self._started = False

    async def configure(self, config, router, session, facades):
        LOG.info('Configuring ExampleConfigPlugin')
        self._config = config
        self._router = router
        self._session = session
        self._facades = facades

        if 'examplelistener' not in self._facades:
            raise ValueError('ExampleListener not in facade')

    async def start(self):
        LOG.info('Starting ExampleConfigPlugin')

        listener_facade = self._facades.get('examplelistener')
        listener_facade.add('sir-bot-a-lot', self.hello_sirbot)

        self._started = True

    async def update(self, config, plugins):
        pass

    @property
    def started(self):
        return self._started

    def facade(self):
        return False

    async def hello_sirbot(self, request, facades):
        name = request.match_info['name']
        LOG.info('''Incoming request to 'hello_sirbot' with name %s''', name)
        sender = facades.get('examplesender')
        rep = await sender.get('https://github.com/ovv/sir-bot-a-lot')

        if rep.status == 200:
            status = 'ok'
        else:
            status = 'to be having problems'

        return Response(text='Hello from {} my github seems {}.'.format(
            name , status))
