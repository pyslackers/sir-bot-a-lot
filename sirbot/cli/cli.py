import argparse
import asyncio
import logging
import sys

from . import config, initialize
from ..core import SirBot


def parse_args(arguments):
    parser = argparse.ArgumentParser(description='The good Sir Bot-a-lot')
    parser.add_argument('-P', '--port', dest='port', action='store',
                        type=int,
                        help='port')
    parser.add_argument('-c', '--config', action='store',
                        help='config file path')
    parser.add_argument('-u', '--update', help='Update plugins',
                        action='store_true', dest='update')
    parser.add_argument('-p', '--plugins', help='Plugins to load',
                        dest='plugins', nargs='+')

    subparsers = parser.add_subparsers(help='Additional commands',
                                       dest='subcommands')

    init_parser = subparsers.add_parser('init',
                                        help='Initialize your Sir Bot-a-lot'
                                             ' configuration')
    init_parser.set_defaults(func=initialize.initialize_plugin)
    init_parser.add_argument('-n', '--name', action='store',
                             help='configuration plugin name')
    init_parser.add_argument('-p', '--plugins', help='Plugins to load',
                             dest='plugins', nargs='+')
    init_parser.add_argument('-P', '--port', dest='port', action='store',
                             type=int, help='port')
    init_parser.add_argument('-l', '--log', dest='log_level', action='store',
                             choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                             help='Logging level', default='INFO')

    return parser.parse_args(arguments)


def main():  # pragma: no cover
    args = parse_args(sys.argv[1:])
    logging.basicConfig()

    if args.subcommands:
        args.func(args)
    else:
        configuration = config.load_config(args)
        if args.update:
            update(configuration)
        else:
            start(configuration)


def start(configuration, loop=None):  # pragma: no cover
    if not loop:
        loop = asyncio.get_event_loop()

    bot = SirBot(config=configuration, loop=loop)
    bot.run(port=int(configuration['sirbot']['port']))
    return bot


def update(configuration, loop=None):
    if not loop:
        loop = asyncio.get_event_loop()

    bot = SirBot(config=configuration, loop=loop)
    loop.run_until_complete(bot.update())
    return bot


if __name__ == '__main__':
    main()  # pragma: no cover
