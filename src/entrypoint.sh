#!/bin/bash

#    python src/manage.py wait_for_db
if [ "$1" == "web" ]; then
    python3 manage.py makemigrations --no-input
    python3 manage.py migrate --no-input
    gunicorn --timeout 1000 --workers=3 --bind=0.0.0.0 --log-level debug config.wsgi:application --reload
elif [ "$1" == "dev" ]; then
    python3 manage.py makemigrations --no-input
    python3 manage.py migrate --no-input
    python3 manage.py runserver 0.0.0.0:"$PORT"
elif [ "$1" == "local" ]; then
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py runserver
fi
