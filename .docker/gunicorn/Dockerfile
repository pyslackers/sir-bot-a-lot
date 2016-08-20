FROM brandsocial/base:python3.5
MAINTAINER Shawn McElroy "shawn@skift.io"

RUN pip3 install gunicorn && \
    mkdir -p /deploy/run

ADD app /deploy/app
ADD requirements /deploy/requirements
ADD gunicorn_config.py /deploy/gunicorn_config.py

WORKDIR /deploy/app
RUN pip3 install -U -r /deploy/requirements/development.txt

# by default gunicorn willgu listen on :5000 so make it available
EXPOSE 5000

CMD ["/usr/local/bin/gunicorn", "-c", "/deploy/gunicorn_config.py", "api:__hug_wsgi__"]
