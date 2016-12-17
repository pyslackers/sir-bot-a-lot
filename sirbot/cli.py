import logging
import os
import argparse

from sirbot import SirBot


def parse_args():
    parser = argparse.ArgumentParser(description='The good Sir-bot-a-lot')
    parser.add_argument('-p', '--port', dest='port', action='store',
                        default=8080, type=int,
                        help='The port to run sirbot')
    parser.add_argument('-c', '--config', action='store',
                        help='Location of the config file')

    return parser.parse_args()


def main():
    args = parse_args()
    logging.basicConfig()

    bot = SirBot(config_file=args.config)
    port = int(os.getenv('PORT', args.port))
    bot.run(port=port)


if __name__ == '__main__':
    main()
