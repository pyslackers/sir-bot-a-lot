FROM sirbot/gunicorn:python3.5
MAINTAINER Shawn McElroy "shawn@skift.io"

ADD app /deploy/app
ADD requirements /deploy/requirements

RUN pip3 install -r /deploy/requirements/development.txt
