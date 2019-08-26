#!/bin/bash

set -o errexit
set -o nounset

python manage.py migrate
python manage.py collectstatic --noinput

#/usr/local/bin/daphne -b 0.0.0.0 -p 5000 config.asgi:application
# we use this now for django channels, versus runserver_plus
python manage.py runserver 0.0.0.0:5000
