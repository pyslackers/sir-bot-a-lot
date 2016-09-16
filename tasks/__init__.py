from invoke import Collection

from tasks import docker
from tasks.base import clean, test, lint, publish, fmt, fmt_dry, swagger

ns = Collection()
ns.add_collection(Collection.from_module(docker))

# we want these to be available at the base level
ns.add_task(clean)
ns.add_task(test)
ns.add_task(lint)
ns.add_task(publish)
ns.add_task(fmt)
ns.add_task(fmt_dry)
ns.add_task(swagger)
