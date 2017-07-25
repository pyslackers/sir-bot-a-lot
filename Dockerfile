FROM python:3.6-alpine

RUN apk add --update --no-cache gcc g++ && pip install dumb-init

COPY sirbot/ /app/sirbot/
COPY requirements/requirements.txt /app/requirements.txt
COPY run.py /app/run.py
RUN python3 -m pip install -r /app/requirements.txt

WORKDIR /app

CMD ["python3", "/app/run.py"]
