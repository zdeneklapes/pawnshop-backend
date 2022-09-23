#!/bin/bash

if [ "$1" == "build" ]; then
    cd backend || exit 1

    python manage.py wait_for_db

    python manage.py collectstatic --no-input

    python manage.py makemigrations --no-input

    python manage.py migrate --no-input

#    gunicorn core.wsgi:application -b 0.0.0.0:"$PORT"
elif [ "$1" == "dev" ]; then
#    python src/manage.py wait_for_db
#    python src/manage.py makemigrations --no-input
#    python src/manage.py migrate --no-input
    poetry run python manage.py runserver 0.0.0.0:"$PORT"
elif [ "$1" == "dev_local" ]; then
    python manage.py wait_for_db

    python manage.py makemigrations --no-input

    python manage.py migrate --no-input

    python manage.py runserver
elif [ "$1" == "prod" ]; then
    python3 backend/manage.py makemigrations --no-input

    python3 backend/manage.py migrate --no-input
fi
