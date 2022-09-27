#!/bin/bash

#    python src/manage.py wait_for_db
if [ "$1" == "web" ]; then
    python manage.py makemigrations --no-input
    python manage.py migrate --no-input
    gunicorn --timeout 1000 --workers=3 --bind=0.0.0.0:$PORT --log-level debug config.wsgi:application --reload
elif [ "$1" == "dev" ]; then
    python manage.py runserver 0.0.0.0:"$PORT"
elif [ "$1" == "local" ]; then
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
fi
