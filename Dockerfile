FROM python:3.6-alpine

RUN apk add --update --no-cache gcc g++ && pip install dumb-init

WORKDIR /app

COPY . .
RUN python3 -m pip install .

COPY config /etc/sirbot
ENV SIRBOT_CONFIG /etc/sirbot/config.yml

VOLUME /var/log/sirbot /etc/sirbot

ENTRYPOINT ["/usr/local/bin/dumb-init", "--"]
CMD ["/bin/sh", "-c", "sirbot --update && exec sirbot"]
