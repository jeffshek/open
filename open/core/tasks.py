from config.celery_app import app


import logging

logger = logging.getLogger(__name__)


@app.task(serializer="json")
def check_services_running():
    return
