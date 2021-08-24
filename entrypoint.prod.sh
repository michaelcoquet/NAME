#!/bin/sh

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py initadmin
gunicorn --bind ${APP_HOST}:8000 NAME.wsgi:application --certfile ssl/fullchain.pem --keyfile ssl/privkey.pem --timeout 300

exec "$@"