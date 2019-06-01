#!/bin/sh

set -o errexit
set -o nounset

rm -f './celerybeat.pid'
rm -f './celerybeat-schedule'

celery -A config.celery_app beat -l INFO
