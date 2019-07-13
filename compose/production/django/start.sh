#!/bin/sh

set -o errexit
set -o nounset


python /app/manage.py collectstatic --noinput

# default to 4 workers
#/usr/local/bin/gunicorn config.wsgi --bind 0.0.0.0:5000 --chdir=/app --workers=4

/usr/local/bin/daphne config.asgi:application -b 0.0.0.0:5000
