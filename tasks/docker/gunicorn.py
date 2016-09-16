from invoke import task

from sirbot import DATA
from tasks.docker import base
from tasks.helpers import (
    container_stop, container_rm, image_rm, image_build,
    get_cache_string
)

NAMESPACE = DATA['author'].lower()
APP = 'gunicorn'
TAG = 'latest'
CACHE = ''


@task(base.build)
def build(ctx, invalidate_cache=False):
    """Build the brand social gunicorn image"""
    tag = '{NAMESPACE}/{APP}:{TAG} .docker/gunicorn'.format(**globals())
    image_build(ctx, tag, get_cache_string(invalidate_cache))


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
