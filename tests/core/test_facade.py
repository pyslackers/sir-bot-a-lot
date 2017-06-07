import pytest
import sirbot

from sirbot.core.errors import FacadeUnavailable
from sirbot.core.facade import MainFacade

from tests.core.test_plugin.sirbot import PluginTest, FacadeTest

config = {
    'loglevel': 10,
    'sirbot': {
        'loglevel': 20,
        'plugins': ['tests.core.test_plugin.sirbot']
    }
}


def test_register_facade(loop):
    bot = sirbot.SirBot(loop=loop, config=config)
    assert 'test' in bot._facades


def test_facade_is_correct_function(loop):
    bot = sirbot.SirBot(loop=loop, config=config)
    assert isinstance(bot._facades.get('test').__self__, PluginTest)
    assert bot._facades.get(
        'test').__qualname__ == PluginTest.facade.__qualname__


def test_main_facade(loop):
    bot = sirbot.SirBot(loop=loop, config=config)
    facade = MainFacade(bot._facades)
    second_facade = facade.new()
    assert isinstance(second_facade, MainFacade)
    assert type(facade) == type(second_facade)


def test_get_facade(loop):
    bot = sirbot.SirBot(loop=loop, config=config)
    facade = MainFacade(bot._facades)
    f = facade.get('test')
    assert isinstance(f, FacadeTest)
    with pytest.raises(FacadeUnavailable) as error:
        facade.get('foo')

    assert error.value.facade == 'foo'


def test_getitem_facade(loop):
    bot = sirbot.SirBot(loop=loop, config=config)
    facade = MainFacade(bot._facades)
    assert isinstance(facade['test'], FacadeTest)
    with pytest.raises(KeyError):
        _ = facade['foo']


def test_contains_facade(loop):
    bot = sirbot.SirBot(loop=loop, config=config)
    facade = MainFacade(bot._facades)
    assert 'test' in facade
    assert 'foo' not in facade


def test_len_facade(loop):
    bot = sirbot.SirBot(loop=loop, config=config)
    facade = MainFacade(bot._facades)
    assert len(facade) == 1


