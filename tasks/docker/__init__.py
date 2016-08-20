from invoke import Collection
from invoke import Failure
from invoke import task

from sirbot import DATA
from tasks.docker import base
from tasks.docker import gunicorn
from tasks.helpers import run_cmd, container_rm, image_rm, container_stop, \
    image_build, get_cache_string, get_tag

ns = Collection()
ns.add_collection(Collection.from_module(base))
ns.add_collection(Collection.from_module(gunicorn))

NAMESPACE = DATA['author'].lower()
APP = 'api'
TAG = 'latest'
CACHE = ''


@task(pre=[gunicorn.build], default=True)
def build(ctx, invalidate_cache=False):
    """Build the brand social app image"""
    tag = '{NAMESPACE}/{APP}:{TAG} .'.format(**globals())
    image_build(ctx, tag, get_cache_string(invalidate_cache))


@task(build)
def up(ctx):
    """Run the brand social image for local dev"""
    cmd = 'docker run ' \
          '--name={APP} ' \
          '--detach=true ' \
          '-v $PWD/app:/deploy/app ' \
          '-p 5000:5000 ' \
          + get_tag(NAMESPACE, APP, TAG)
    cmd = cmd.format(**globals())
    # cmd = "docker-compose up"
    run_cmd(ctx, cmd)


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


@task
def reset(ctx):
    try:
        run_cmd(ctx, 'docker stop api')
    except Failure:
        pass
    try:
        run_cmd(ctx, 'docker rm   api')
    except Failure:
        pass
    try:
        run_cmd(ctx, 'docker rmi  {}/api'.format(NAMESPACE))
    except Failure:
        pass
    try:
        run_cmd(ctx, 'docker rmi {}/gunicorn'.format(NAMESPACE))
    except Failure:
        pass
    try:
        run_cmd(ctx, 'docker rmi {}/base:python3.5'.format(NAMESPACE))
    except Failure:
        pass


ns.add_task(build)
ns.add_task(up)
ns.add_task(rm)
ns.add_task(rmi)
ns.add_task(reset)
