import os
import yaml


def load_config(args):

    path = args.config or os.getenv('SIRBOT_CONFIG')
    port = args.port or os.getenv('SIRBOT_PORT')
    config = load_file(path)

    if 'sirbot' not in config:
        config['sirbot'] = dict()

    if args.plugins:
        if 'plugins' not in config['sirbot']:
            config['sirbot']['plugins'] = list()
        config['sirbot']['plugins'].extend(args.plugins)

    if port:
        config['sirbot']['port'] = port
    elif 'port' not in config['sirbot']:
        config['sirbot']['port'] = 8080

    return config


def load_file(path=None):

    if not path:
        return dict()
    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)

    with open(path) as file:
        return yaml.load(file)
