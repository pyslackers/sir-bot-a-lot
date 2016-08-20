from invoke import task

from sirbot import DATA
from tasks.helpers import container_stop, container_rm, image_rm, image_build

NAMESPACE = DATA['author'].lower()
APP = 'base'
TAG = 'python3.5'
CACHE = ''


@task
def build(ctx, invalidate_cache=False):
    """Build the brand social base image"""
    tag = '{NAMESPACE}/{APP}:{TAG} .docker/base'.format(**globals())
    image_build(ctx, tag, invalidate_cache)


@task
def stop(ctx):
    """stop the currently running container"""
    container_stop(ctx, '{NAMESPACE}/{APP}'.format(**globals()))


@task(stop)
def rm(ctx):
    """Delete the currently running container"""
    container_rm(ctx, '{NAMESPACE}/{APP}'.format(**globals()))


@task(rm)
def rmi(ctx):
    """delete the current image"""
    image_rm(ctx, '{NAMESPACE}/{APP}:{TAG}'.format(**globals()))
