# -*- coding: utf-8 -*-
"""
test_sirbot
----------------------------------

Tests for `sirbot` module.
"""
import sirbot
import pytest

from copy import deepcopy
from aiohttp.web import Response

from sirbot.facade import MainFacade

from tests.test_plugin.sirbot import PluginTest

CONFIG = {
    'loglevel': 10,
    'core': {
        'loglevel': 20,
        'plugins': ['tests.test_plugin.sirbot']
    },
    'test': {
        'test_config': True
    }
}

async def test_bot_is_starting(loop, test_server):
    bot = sirbot.SirBot(loop=loop)
    await test_server(bot._app)
    assert bot._app == bot.app

async def test_load_config(loop):
    config = {
        'loglevel': 10,
        'core': {
            'loglevel': 20,
            'plugins': ['tests.test_plugin']
        }
    }
    bot = sirbot.SirBot(loop=loop, config=config)
    assert bot.config == config

async def test_plugin_import(loop, test_server):
    bot = sirbot.SirBot(loop=loop, config=CONFIG)
    await test_server(bot._app)
    assert bot._pm.has_plugin('tests.test_plugin.sirbot')

async def test_plugin_import_error(loop):
    bot = sirbot.SirBot(loop=loop)
    bot.config['core'] = {
        'plugins': ['xxx', ]
    }
    with pytest.raises(ImportError):
        bot._import_plugins()

async def test_initialize_plugins(loop):
    bot = sirbot.SirBot(loop=loop, config=CONFIG)
    assert isinstance(bot._plugins.get('test'), PluginTest)

async def test_plugin_configure(loop):
    bot = sirbot.SirBot(loop=loop, config=CONFIG)
    assert bot._plugins.get('test').config == CONFIG['test']

async def test_start_plugins(loop, test_server):
    bot = sirbot.SirBot(loop=loop, config=CONFIG)
    await test_server(bot._app)
    assert 'test' in bot._tasks

async def test_plugin_task_error(loop, test_server, capsys):
    config = deepcopy(CONFIG)
    config['core']['plugins'] = ['tests.test_plugin.sirbot_start_error']
    bot = sirbot.SirBot(loop=loop, config=config)
    await test_server(bot._app)
    out, err = capsys.readouterr()
    del bot._tasks['test']
    assert 'Task exited with error' in err

async def test_middleware(loop, test_client):

    async def handler(request):
        assert isinstance(request['facades'], MainFacade)
        return Response(text='test')

    bot = sirbot.SirBot(loop=loop, config=CONFIG)
    bot._app.router.add_route('GET', '/', handler)
    server = await test_client(bot._app)
    rep = await server.get('/')
    assert 200 == rep.status
    assert 'test' == (await rep.text())
