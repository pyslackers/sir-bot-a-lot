import sirbot
import asyncio

from tests.test_plugin.dispatcher import Dispatcher
from tests.test_plugin.facade import TestFacade


async def test_intialize_dispatcher(loop, test_server):
    bot = sirbot.SirBot(loop=loop, config_file='tests/test_config.yml')
    await test_server(bot._app)
    assert isinstance(bot._dispatcher._dispatchers.get('test')[0], Dispatcher)

async def test_queue_and_dispatcher(loop, test_server):
    bot = sirbot.SirBot(loop=loop, config_file='tests/test_config.yml')
    await test_server(bot._app)
    test_dispatcher = bot._dispatcher._dispatchers.get('test')[0]
    await bot._incoming_queue.put(('test', {'a': 1}))

    await asyncio.sleep(0.3, loop=loop)
    assert test_dispatcher.msg[0][0] == {'a': 1}
    assert isinstance(test_dispatcher.msg[0][1], TestFacade)
    assert isinstance(test_dispatcher.msg[0][2], sirbot.facade.MainFacade)

async def test_error_in_dispatcher(loop, test_server, capsys):
    bot = sirbot.SirBot(loop=loop, config_file='tests/test_config.yml')
    await test_server(bot._app)
    await bot._incoming_queue.put(('test', 'error'))
    await asyncio.sleep(0.3, loop=loop)
    _, err = capsys.readouterr()
    assert 'There was an issue' in err