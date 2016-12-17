import sirbot
import asyncio

from tests.test_plugin.dispatcher import Dispatcher
from tests.test_plugin.facade import TestFacade


async def test_facades_are_different(loop, test_server):
    bot = sirbot.SirBot(loop=loop, config_file='tests/test_config.yml')
    await test_server(bot._app)
    test_dispatcher = bot._dispatcher._dispatchers.get('test')[0]
    await bot._incoming_queue.put(('test', {'a': 1}))
    await bot._incoming_queue.put(('test', {'b': 2}))
    await asyncio.sleep(0.3, loop=loop)
    assert test_dispatcher.msg[0][0] != test_dispatcher.msg[1][0]
    assert test_dispatcher.msg[0][1] != test_dispatcher.msg[1][1]
    assert test_dispatcher.msg[0][2] != test_dispatcher.msg[1][2]

async def test_get_facade(loop, test_server):
    bot = sirbot.SirBot(loop=loop, config_file='tests/test_config.yml')
    await test_server(bot._app)
    test_dispatcher = bot._dispatcher._dispatchers.get('test')[0]
    await bot._incoming_queue.put(('test', {'a': 1}))
    await asyncio.sleep(0.3, loop=loop)
    test_facade = test_dispatcher.msg[0][2].get('test')
    assert isinstance(test_facade, TestFacade)
    no_facade = test_dispatcher.msg[0][2].get('no facade')
    assert no_facade is None