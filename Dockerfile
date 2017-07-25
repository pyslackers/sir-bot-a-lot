FROM python:3.6-alpine

RUN apk add --update --no-cache gcc g++ && pip install dumb-init

WORKDIR /app

COPY . .
RUN python3 -m pip install .

ENTRYPOINT ["/usr/local/bin/dumb-init", "--"]
CMD ["sirbot"]
