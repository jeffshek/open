#!/bin/bash

set -o errexit
set -o nounset


python /app/manage.py collectstatic --noinput
python manage.py migrate --no-input

# default to 4 workers
#/usr/local/bin/gunicorn config.wsgi --bind 0.0.0.0:5000 --chdir=/app --workers=4

/usr/local/bin/daphne -b 0.0.0.0 -p 5000 config.asgi:application
