# #!/bin/sh

# until python3 manage.py celery -A project inspect ping; do
#     >&2 echo "Celery workers not available"
# done

# echo 'Starting flower'
# python3 manage.py celery -A project flower

# exec "$@"