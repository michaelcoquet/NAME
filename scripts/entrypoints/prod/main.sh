#!/bin/sh
cd ../../
# python3 manage.py collectstatic --no-input
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py initadmin
gunicorn --bind ${APP_HOST}:8000 NAME.wsgi:application --certfile ssl/prod/fullchain.pem --keyfile ssl/prod/privkey.pem --timeout 300

exec "$@"