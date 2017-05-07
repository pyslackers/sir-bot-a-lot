import yaml

from sirbot.core import cli

CONFIG = {'loglevel': 10,
          'core': {'plugins': ['tests.core.test_plugin.sirbot'], 'loglevel': 20}}


def test_argument_parser_config():
    args = cli.parse_args(['-c', 'config.yml'])
    assert args.config == 'config.yml'


def test_argument_parser_port():
    args = cli.parse_args(['-P', '4567'])
    assert args.port == 4567


def test_load_config_file():
    config_file = 'tests/core/test_config.yml'
    config = cli.load_config(config_file)
    with open(config_file) as f:
        data = yaml.load(f)
    assert config == data


def test_no_config_file():
    config = cli.load_config()
    assert config == {}


def test_plugin_arg():
    args = cli.parse_args(['-p', 'xxx', 'yyy'])
    assert args.plugins == ['xxx', 'yyy']

    config = cli.cli_plugin(args, {})
    assert config == {'sirbot': {'plugins': ['xxx', 'yyy']}}

    config_2 = cli.cli_plugin(args, {'sirbot': {}})
    assert config_2 == {'sirbot': {'plugins': ['xxx', 'yyy']}}

    config_3 = cli.cli_plugin(args, {'sirbot': {'plugins': ['aaa']}})
    assert config_3 == {'sirbot': {'plugins': ['aaa', 'xxx', 'yyy']}}
