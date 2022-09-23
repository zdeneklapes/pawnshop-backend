FROM python:3

#####################################

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip3 install poetry && \
    poetry install --no-root

ENV PORT 8000
EXPOSE 8000

#####################################

WORKDIR /app/src

COPY src/ .

RUN chmod +x entrypoint.sh
ENTRYPOINT [ "/app/src/entrypoint.sh", "dev"]

## Use an official Python runtime as a parent image - Build stage
##FROM python:3.10.5-alpine as build-image
##
##ENV PYTHONUNBUFFERED=1
##ENV PIPENV_VENV_IN_PROJECT=1
##
##COPY Pipfile .
##
### Install packages only needed in build stage
##RUN  \
##    apk update && \
##    apk upgrade && \
##    apk add --virtual .build-deps gcc musl-dev postgresql-libs postgresql-dev && \
##    pip3 install pipenv && \
##    pipenv install --dev --deploy --python 3.10 && \
##    apk --purge del .build-deps
##
### Use an official Python runtime as a parent image - Run stage
##FROM python:3.10.5-alpine as runtime
##
##ENV PYTHONUNBUFFERED=1
##
### Copy venv from build stage
##COPY --from=build-image /.venv /.venv
##ENV PATH="/.venv/bin:$PATH"
##
### Install packages that are only needed runtime
##RUN  \
##    apk update && \
##    apk upgrade && \

##    apk add bash postgresql-libs && \
##    rm -rf /var/cache/apk/*
##
### Add the rest of the code
##COPY . /app/backend
##COPY ./scripts/ /app/
##
### Make port 8000 available for the app
##ENV PORT 8000
##EXPOSE 8000
##
### Change directory so that scripts could locate manage.py
##WORKDIR /app/backend
##
### Be sure to use 0.0.0.0 for the host within the Docker container,
### otherwise the browser won't be able to find it
##RUN ["chmod", "+x", "/app/entrypoint-dev.sh"]
##ENTRYPOINT [ "/app/entrypoint-dev.sh" ]
#
## The base image we want to inherit from
#FROM python:3.7.7-slim-buster AS development_build
#
#ARG DJANGO_ENV
#
#ENV DJANGO_ENV=${DJANGO_ENV} \
#  # python:
#  PYTHONFAULTHANDLER=1 \
#  PYTHONUNBUFFERED=1 \
#  PYTHONHASHSEED=random \
#  # pip:
#  PIP_NO_CACHE_DIR=off \
#  PIP_DISABLE_PIP_VERSION_CHECK=on \
#  PIP_DEFAULT_TIMEOUT=100 \
#  # poetry:
#  POETRY_VERSION=1.0.5 \
#  POETRY_VIRTUALENVS_CREATE=false \
#  POETRY_CACHE_DIR='/var/cache/pypoetry'
#
## System deps:
#RUN apt-get update \
#  && apt-get install --no-install-recommends -y \
#    bash \
#    build-essential \
#    curl \
#    gettext \
#    git \
#    libpq-dev \
#    wget \
#  # Cleaning cache:
#  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
#  && pip install "poetry==$POETRY_VERSION" && poetry --version
#
## set work directory
#WORKDIR /app
#COPY pyproject.toml poetry.lock /app/
#
## Install dependencies:
#RUN poetry install
## copy project
#COPY src/ .
#
##RUN chmod +x /app/entrypoint.sh
##ENTRYPOINT [ "/app/entrypoint.sh", "dev"]
