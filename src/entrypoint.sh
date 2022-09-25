#!/bin/bash

if [ "$1" == "build" ]; then
    python manage.py migrate --no-input
    python manage.py makemigrations --no-input
elif [ "$1" == "dev" ]; then
    #    python3 src/manage.py wait_for_db
#    python3 manage.py migrate --no-input
#    python3 manage.py makemigrations --no-input
#    gunicorn --timeout 1000 --workers=3 --bind=0.0.0.0:$PORT --log-level debug src.wsgi:application
#    poetry run python manage.py runserver 0.0.0.0:"$PORT"
    python manage.py wait_for_db
    python manage.py runserver
fi
