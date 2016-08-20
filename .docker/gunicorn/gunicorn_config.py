# to tune see http://gunicorn-docs.readthedocs.org/en/latest/settings.html

import multiprocessing
import os

# to serve directly via TCP:
bind = os.getenv('GUNICORN_BIND', '0.0.0.0:5000')
# for nginx or other proxy:
# bind = "unix:/deploy/run/gunicorn.sock"
#
workers = os.getenv('GUNICORN_WORKERS', (multiprocessing.cpu_count() * 2 + 1))
# should save some memory:
preload_app = True

worker_class = 'sync'
# only relevant for async workers:
#worker_connections = 1000

user = 'root'
group = 'root'

# set this if workers appear to leak memory or have some other longer-lived
# problem. Then they'll automatically restart after they've serviced this many
# requests:
# max_requests = 1000

# logging:
# accesslog = '/deploy/logs/gunicorn.access.log'
# errorlog = '/deploy/logs/gunicorn.error.log'
# loglevel = 'info'

# where to store the PID file:

pidfile = '/deploy/run/gunicorn.pid'

# Defaults is 30.  This is how long the master will wait to hear from a worker
# before killing it.  Can set higher if there are some longer running requests:
# timeout = 28

# only use for development:
# reload = True

# for performance:
keepalive = os.getenv('GUNICORN_KEEPALIVE', 3)
