#!/bin/sh

set -o errexit
set -o nounset

python manage.py migrate
python manage.py collectstatic --noinput

# we use this now for django channels, versus runserver_plus
python manage.py runserver 0.0.0.0:8008

#python manage.py runserver_plus 0.0.0.0:8008
