import logging
import os
import sys
import argparse
import yaml
import asyncio

from sirbot import SirBot


def parse_args(arguments):
    parser = argparse.ArgumentParser(description='The good Sir-bot-a-lot')
    parser.add_argument('-p', '--port', dest='port', action='store',
                        type=int,
                        help='port where to run sirbot')
    parser.add_argument('-c', '--config', action='store',
                        help='path to the Yaml config file')

    return parser.parse_args(arguments)


def load_config(path=None):
    if path:
        with open(path) as file:
            return yaml.load(file)
    return {}


def start(config, loop=None):  # pragma: no cover
    if not loop:
        loop = asyncio.get_event_loop()
    bot = SirBot(config=config, loop=loop)
    bot.run(port=int(config.get('port', 8080)))
    return bot


def main():  # pragma: no cover
    args = parse_args(sys.argv[1:])
    logging.basicConfig()

    config_file = os.getenv('SIRBOT_CONFIG', args.config)
    config = load_config(config_file)
    config['port'] = os.getenv('SIRBOT_PORT') or args.port or config.get(
        'port') or 8080
    start(config)


if __name__ == '__main__':
    main()  # pragma: no cover
