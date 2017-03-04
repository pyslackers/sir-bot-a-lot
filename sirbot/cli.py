import logging
import os
import argparse
import yaml

from sirbot import SirBot


def parse_args():
    parser = argparse.ArgumentParser(description='The good Sir-bot-a-lot')
    parser.add_argument('-p', '--port', dest='port', action='store',
                        type=int,
                        help='port where to run sirbot')
    parser.add_argument('-c', '--config', action='store',
                        help='path to the Yaml config file')

    return parser.parse_args()


def main():
    args = parse_args()
    logging.basicConfig()

    config_file = os.getenv('SIRBOT_CONFIG', args.config)
    if config_file:
        with open(config_file) as file:
            config = yaml.load(file)
    else:
        config = dict()

    port = int(os.getenv('SIRBOT_PORT')) or int(args.port) or config.get(
        'port') or 8080

    bot = SirBot(config=config)
    bot.run(port=port)


if __name__ == '__main__':
    main()
