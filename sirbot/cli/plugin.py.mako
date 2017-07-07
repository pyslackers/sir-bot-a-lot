from sirbot.core import hookimpl, Plugin


@hookimpl
def plugins(loop):
    return ${name}(loop)


class ${name}(Plugin):
    """
    Configuration plugin.
    """

    __version__ = '0.0.1'
    __name__ = '${name}'

    def __init__(self, loop):
        super().__init__(loop)
        self._loop = loop

        self._config = None
        self._router = None
        self._session = None
        self._registry = None

        self._started = False

    async def configure(self, config, router, session, registry):
        super().__init__(config, router, session, registry)
        self._config = config  # ${name} plugin configuration
        self._router = router  # aiohttp router
        self._session = session  # aiohttp session
        self._registry = registry

    async def start(self):

        #
        # Your business logic goes here
        #

        # Your plugin is successfully started
        self._started = True

    @property
    def started(self):
        return self._started
