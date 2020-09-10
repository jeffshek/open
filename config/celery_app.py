import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

MINUTES_INTERVAL = 60

app = Celery("open")

app.conf.beat_schedule = {
    "check-all-services-running": {
        "task": "open.core.tasks.check_services_running",
        # run every 30 minutes to make sure all the ml-services are running
        "schedule": 30 * MINUTES_INTERVAL,
    },
    "reset-betterself-demo-fixtures": {
        "task": "open.core.tasks.reset_betterself_demo_fixtures",
        "schedule": 30 * MINUTES_INTERVAL,
    },
}

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
