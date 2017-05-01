import pytest
import asyncio
import yaml

from sirbot import cli

CONFIG = {'loglevel': 10,
          'core': {'plugins': ['tests.test_plugin.sirbot'], 'loglevel': 20}}


def test_argument_parser_config():
    args = cli.parse_args(['-c', 'config.yml'])
    assert args.config == 'config.yml'


def test_argument_parser_port():
    args = cli.parse_args(['-P', '4567'])
    assert args.port == 4567


def test_load_config_file():
    config_file = 'tests/test_config.yml'
    config = cli.load_config(config_file)
    with open(config_file) as f:
        data = yaml.load(f)
    assert config == data


def test_no_config_file():
    config = cli.load_config()
    assert config == {}
