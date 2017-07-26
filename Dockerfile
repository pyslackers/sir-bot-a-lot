FROM python:3.6-alpine

RUN apk add --update --no-cache gcc g++ && pip install dumb-init

WORKDIR /app

COPY . .
RUN python3 -m pip install .

COPY docker.yml /etc/sirbot.yml

ENTRYPOINT ["/usr/local/bin/dumb-init", "--"]
CMD ["/bin/sh", "-c", "sirbot -c /etc/sirbot.yml --update && exec sirbot -c /etc/sirbot.yml"]
