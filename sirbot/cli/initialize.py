import os

from mako.template import Template


def initialize_plugin(args):
    try:
        config = make_config(args)
        generate_yaml(config)
        generate_python(config)
    except KeyboardInterrupt:
        pass


def make_config(args):
    config = {
        'name': args.name,
        'plugins': args.plugins,
        'port': args.port,
        'log_level': args.log_level
    }

    if not config['name']:
        while True:
            name = input('Configuration plugin name: ')
            if len(name) > 0:
                break
        config['name'] = name.lower().replace(' ', '_').strip()

    if not config['plugins']:
        plugins = input('Plugins to load (comma separated list): ')

        if plugins:
            config['plugins'] = set(
                plugin.strip() for plugin in plugins.split(',')
            )
        else:
            print('No plugins will be configured')
    else:
        config['plugins'] = set(config['plugins'])
    config['plugins'].add(config['name'])

    if not config['port']:
        while True:
            try:
                port = int(input('Sir Bot-a-lot port: '))
            except ValueError:
                print('Please enter an integer')
            else:
                config['port'] = port
                break

    return config


def generate_yaml(config):
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'sirbot.yml.mako'
    )

    config_template = Template(filename=path)
    config_render = config_template.render(**config)

    with open('sirbot.yml', 'w') as file:
        file.write(config_render)


def generate_python(config):
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'plugin.py.mako'
    )

    plugin_template = Template(filename=path)
    plugin_render = plugin_template.render(**config)

    with open('{}.py'.format(config['name']), 'w') as file:
        file.write(plugin_render)
