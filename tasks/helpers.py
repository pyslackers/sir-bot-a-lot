from colorama import Fore
from invoke import Failure

from sirbot import DATA

DOCKER = {
    "NAMESPACE": DATA['author'].lower(),
    "APP": DATA['docker_name'].lower(),
    "TAG": DATA['docker_tag'].lower(),
}

CACHE = ''


def run_cmd(ctx, cmd):
    print(Fore.LIGHTYELLOW_EX + " > " + cmd + Fore.RESET)
    ctx.run(cmd)


def container_stop(ctx, tag):
    print(Fore.LIGHTRED_EX + " > STOPPING : " + tag + Fore.RESET)
    update_instance(ctx, 'stop', tag)


def container_rm(ctx, tag):
    print(Fore.LIGHTRED_EX + " > REMOVING : " + tag + Fore.RESET)
    update_instance(ctx, 'rm', tag)


def image_rm(ctx, tag):
    print(Fore.LIGHTRED_EX + " > REMOVING : " + tag + Fore.RESET)
    update_instance(ctx, 'rmi', tag)


def image_build(ctx, tag, invalidate_cache=False):
    cmd = 'docker build {} -t {}'.format(
        get_cache_string(invalidate_cache), tag)
    run_cmd(ctx, cmd)


def update_instance(ctx, type, tag):
    try:
        cmd = 'docker {type} {tag}'.format(type=type, tag=tag)
        run_cmd(ctx, cmd)
    except Failure as err:
        pass


def get_cache_string(invalidate=False):
    return '--no-cache=true' if invalidate else ''


def get_tag(ns, app, tag='latest'):
    text = '{ns}/{app}:{tag}'
    return text.format(**locals())
