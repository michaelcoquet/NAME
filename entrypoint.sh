#!/bin/sh

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done

python3 manage.py flush --no-input
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py initadmin
python3 -m ptvsd --host 0.0.0.0 --port 3000 manage.py runserver_plus --cert-file cert.crt 0.0.0.0:8000 --noreload --nothreading

exec "$@"