#!/bin/sh

until celery -A NAME inspect ping; do
    >&2 echo "Celery workers not available"
done

echo 'Starting flower'
celery -A NAME flower
