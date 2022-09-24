##### VENV
FROM python:3

#####################################

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN set -ex && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

ENV PORT 8000
ENV DOCKER_CONTAINER Yes
EXPOSE 8000

#####################################

WORKDIR /app/src

COPY src/ .

#CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "src.wsgi:application"]
#CMD ["gunicorn", "--timeout", "1000", "--workers=3", "--bind=:8000","--log-level", "debug", "src.wsgi:application"]
#CMD gunicorn --timeout 1000 --workers=3 --bind=0.0.0.0:$PORT --log-level debug src.wsgi:application
RUN chmod +x entrypoint.sh
ENTRYPOINT [ "/app/src/entrypoint.sh", "dev"]





##### PEOTRY
#FROM python:3
#
######################################
#
#ENV PYTHONUNBUFFERED 1
#
#WORKDIR /app
#
#COPY poetry.lock pyproject.toml /app/
#
#RUN pip3 install poetry && \
#    poetry install --no-root
#
#ENV PORT 8000
#EXPOSE 8000
#
######################################
#
#WORKDIR /app/src
#
#COPY src/ .
#
#RUN chmod +x entrypoint.sh
#ENTRYPOINT [ "/app/src/entrypoint.sh", "dev"]
