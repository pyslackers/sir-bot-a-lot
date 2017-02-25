from sirbot.hookimpl import hookimpl
from .client import Client
from .dispatcher import Dispatcher


@hookimpl
def clients(loop, queue):
    return 'test', Client(loop=loop)


@hookimpl
def dispatchers(loop):
    return 'test', Dispatcher(loop=loop)
