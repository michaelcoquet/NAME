#!/bin/sh

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done

# python3 manage.py flush --no-input # comment to persist data in the database
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py initadmin
python3 -m ptvsd --host ${APP_HOST} --port 3000 manage.py runserver_plus --cert-file ssl/name.crt ${APP_HOST}:8000 --noreload --nothreading

exec "$@"