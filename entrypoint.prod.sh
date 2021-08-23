#!/bin/sh

# while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
#   sleep 0.1
# done

# python3 manage.py flush --no-input # comment to persist data in the database
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py initadmin
gunicorn --bind ${APP_HOST}:8000 NAME.wsgi:application --timeout 300
# python3 manage.py runserver_plus ${APP_HOST}:8000 --noreload --nothreading

exec "$@"