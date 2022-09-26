#!/bin/bash

if [ "$1" == "web" ]; then
    python manage.py makemigrations --no-input
    python manage.py migrate --no-input
    gunicorn --timeout 1000 --workers=3 --bind=0.0.0.0:$PORT --log-level debug config.wsgi:application --reload
elif [ "$1" == "dev" ]; then
#    python src/manage.py wait_for_db
    python manage.py runserver 0.0.0.0:"$PORT"
fi
