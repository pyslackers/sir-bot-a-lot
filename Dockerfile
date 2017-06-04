FROM python:3.6-alpine

ENV PYTHONPATH=./.pip:/app/.pip:.: \
    DOCKER=True
COPY . /app/
RUN python3 -m pip install -r /app/requirements/requirements.txt -t /app/.pip


WORKDIR /app

CMD ["python", "./run.py"]
