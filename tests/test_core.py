# -*- coding: utf-8 -*-
"""
test_sirbot
----------------------------------

Tests for `sirbot` module.
"""
import sirbot
import pytest

from tests.test_plugin.client import Client

async def test_bot_is_starting(loop, test_server):
    bot = sirbot.SirBot(loop=loop)
    await test_server(bot._app)
    assert bot._app == bot.app
    assert bot._incoming_queue
    assert bot._dispatcher
    assert 'incoming' in bot._tasks

async def test_load_config(loop):
    config = {
        'loglevel': 10,
        'core': {
            'loglevel': 20,
            'plugins': ['tests.test_plugin']
        }
    }
    bot = sirbot.SirBot(loop=loop, config_file='tests/test_config.yml')
    assert bot.config == config

async def test_plugin_import(loop, test_server):
    bot = sirbot.SirBot(loop=loop, config_file='tests/test_config.yml')
    await test_server(bot._app)
    assert bot._pm.has_plugin('tests.test_plugin')

async def test_plugin_import_error(loop):
    bot = sirbot.SirBot(loop=loop)
    bot.config['core'] = {
        'plugins': ['xxx', ]
    }
    with pytest.raises(ImportError):
        bot._import_plugins()

async def test_initialize_clients(loop, test_server):
    bot = sirbot.SirBot(loop=loop, config_file='tests/test_config.yml')
    await test_server(bot._app)
    await bot._initialize_clients()
    assert isinstance(bot._clients.get('test'), Client)
