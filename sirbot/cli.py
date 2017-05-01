import logging
import os
import sys
import argparse
import yaml
import asyncio

from sirbot import SirBot


def parse_args(arguments):
    parser = argparse.ArgumentParser(description='The good Sir-bot-a-lot')
    parser.add_argument('-P', '--port', dest='port', action='store',
                        type=int,
                        help='port where to run sirbot')
    parser.add_argument('-c', '--config', action='store',
                        help='path to the Yaml config file')
    parser.add_argument('-u', '--update', help='Run update of plugins'
                                               'if necessary',
                        action='store_true', dest='update')
    parser.add_argument('-p', '--plugins', help='Plugins to load',
                        dest='plugins', nargs='+')

    return parser.parse_args(arguments)


def load_config(path=None):

    if not path:
        return dict()
    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)

    with open(path) as file:
        return yaml.load(file)


def cli_plugin(args, config):
    if args.plugins:
        try:
            config['sirbot']['plugins'].extend(args.plugins)
        except KeyError:
            if 'sirbot' not in config:
                config['sirbot'] = {'plugins': []}
            elif 'plugins' not in config['sirbot']:
                config['sirbot']['plugins'] = list()

            config['sirbot']['plugins'] = args.plugins

    return config


def main():  # pragma: no cover
    args = parse_args(sys.argv[1:])
    logging.basicConfig()

    config_file = args.config or os.getenv('SIRBOT_CONFIG')
    config = load_config(config_file)
    config = cli_plugin(args, config)

    try:
        port = args.port or config['sirbot']['port']
    except KeyError:
        port = 8080

    try:
        if args.update:
            update(config)
        else:
            start(config, port=port)
    except Exception as e:
        raise


def start(config, port, loop=None):  # pragma: no cover
    if not loop:
        loop = asyncio.get_event_loop()
    bot = SirBot(config=config, loop=loop)
    bot.run(port=int(port))
    return bot


def update(config, loop=None):
    if not loop:
        loop = asyncio.get_event_loop()
    bot = SirBot(config=config, loop=loop)
    loop.run_until_complete(bot.update())
    return bot


if __name__ == '__main__':
    main()  # pragma: no cover
