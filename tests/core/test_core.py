# -*- coding: utf-8 -*-
"""
test_sirbot
----------------------------------

Tests for `sirbot` module.
"""
import logging
import pytest
import sirbot

from copy import deepcopy

from tests.core.test_plugin.sirbot import PluginTest

CONFIG = {
    'sirbot': {
        'plugins': ['tests.core.test_plugin.sirbot']
    },
    'test': {
        'test_config': True
    }
}


def test_bot_is_starting(loop, test_server):
    bot = sirbot.SirBot(loop=loop)
    loop.run_until_complete(test_server(bot._app))
    assert bot._app == bot.app


def test_load_config(loop):
    config = {
        'sirbot': {
            'plugins': ['tests.core.test_plugin']
        }
    }
    bot = sirbot.SirBot(loop=loop, config=config)
    assert bot.config == config


def test_logging_config(loop):
    config = {
        'logging': {
            'version': 1,
            'loggers': {
                'sirbot.core': {
                    'level': 'WARNING'
                },
                'sirbot': {
                    'level': 'ERROR'
                }
            }
        },
        'sirbot': {
            'plugins': ['tests.core.test_plugin.sirbot']
        }
    }
    bot = sirbot.SirBot(loop=loop, config=config)
    assert logging.getLogger('sirbot.core').level == 30
    assert logging.getLogger('sirbot').level == 40


def test_plugin_import(loop, test_server):
    bot = sirbot.SirBot(loop=loop, config=CONFIG)
    loop.run_until_complete(test_server(bot._app))
    assert bot._pm.has_plugin('tests.core.test_plugin.sirbot')


def test_plugin_import_error(loop):
    bot = sirbot.SirBot(loop=loop)
    bot.config['sirbot'] = {
        'plugins': ['xxx', ]
    }
    with pytest.raises(ImportError):
        bot._import_plugins()


def test_initialize_plugins(loop):
    bot = sirbot.SirBot(loop=loop, config=CONFIG)
    assert isinstance(bot._plugins['test']['plugin'], PluginTest)


def test_plugin_configure(loop, test_server):
    bot = sirbot.SirBot(loop=loop, config=CONFIG)
    loop.run_until_complete(bot._configure_plugins())

    assert bot._plugins['test']['plugin'].config == CONFIG['test']


def test_start_plugins(loop, test_server):
    bot = sirbot.SirBot(loop=loop, config=CONFIG)
    loop.run_until_complete(test_server(bot._app))
    assert 'test' in bot._tasks


def test_plugin_task_error(loop, test_server, capsys):
    config = deepcopy(CONFIG)
    config['sirbot']['plugins'] = ['tests.core.test_plugin.sirbot_start_error']
    bot = sirbot.SirBot(loop=loop, config=config)
    with pytest.raises(ValueError):
        loop.run_until_complete(test_server(bot._app))


def test_plugin_priority(loop, test_server):
    config = deepcopy(CONFIG)
    config['test']['priority'] = 80
    config['test-error'] = {'priority': 70}
    config['sirbot']['plugins'].append('tests.core.test_plugin.sirbot_start_error')
    bot = sirbot.SirBot(loop=loop, config=config)
    assert bot._start_priority[80] == ['test']
    assert bot._start_priority[70] == ['test-error']


def test_plugin_no_start(loop, test_server):
    config = deepcopy(CONFIG)
    config['test']['priority'] = False
    bot = sirbot.SirBot(loop=loop, config=config)
    assert bot._start_priority == {}
    assert bot._plugins == {}
