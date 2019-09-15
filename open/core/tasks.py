from config.celery_app import app


import logging

logger = logging.getLogger(__name__)


@app.task(serializer="json")
def check_services_running():
    logger.exception("Check Celery Will Route to Sentry")
    raise ValueError("Check Raised Exceptions Route to Sentry")
