FROM python:3.9 AS base

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    pip3 install poetry && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*
RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-dev --no-root --no-ansi --no-interaction

COPY ./app ./app

FROM base AS app

COPY entrypoint.sh .env ./
