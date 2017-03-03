import logging
import asyncio

from collections import defaultdict

from .facade import MainFacade

logger = logging.getLogger('sirbot.core')


class Dispatcher:
    def __init__(self, pm, config, loop):
        """
        Core dispatcher for the incoming messages
        """
        self._pm = pm
        self._loop = loop or asyncio.get_event_loop()
        self._config = config
        self._facades = dict()
        self._dispatchers = defaultdict(list)
        self._start_dispatchers()

    async def incoming_message(self, receiver, message) -> None:
        """
        Dispatch the message to the correct module

        Match the message based on the receiver and the dispatcher name.
        Send the module dispatcher the messages and the facades

        :param receiver: Name of the receiver. Should match the dispatcher
        name.
        :param message: Incoming message
        :return:
        """
        dispatchers = self._dispatchers.get(receiver)
        if dispatchers:
            for dispatcher in dispatchers:
                try:
                    facade = MainFacade(self._facades)
                    await dispatcher.incoming(message,
                                              facade.get(receiver),
                                              facade)
                except Exception as e:
                    logger.exception('There was an issue %s with dispatcher '
                                     '%s', e, dispatcher)
        else:
            logger.error('No dispatcher found for %s', receiver)

    def _start_dispatchers(self) -> None:
        """
        Load the modules dispatcher

        There should be one dispatcher by receiver
        """
        logger.debug('Initializing dispatchers')
        dispatchers = self._pm.hook.dispatchers(loop=self._loop)

        if dispatchers:
            for dispatcher in dispatchers:
                self._dispatchers[dispatcher[0]].append(dispatcher[1])
                self._facades[dispatcher[0]] = dispatcher[1].facade
                dispatcher[1].configure(self._config.get(dispatcher[0]))
        else:
            logger.error('No dispatchers found')

    async def middleware_factory(self, app, handler):
        async def middleware_handler(request):
            return await handler(request, MainFacade(self._facades))
        return middleware_handler
