from config.celery_app import app
from django.conf import settings
import logging
import requests

from config.constants import PRODUCTION

logger = logging.getLogger(__name__)


@app.task(serializer="json")
def check_services_running():
    if settings.ENVIRONMENT != PRODUCTION:
        return

    post_data = {
        "prompt": "We know that this is an important moment in the history of our country he said. We are proud to support the work of the American Civil Liberties Union and we will continue to fight for the rights of all Americans. The ACLU is currently suing the government over its surveillance programs. The ACLU said it had been monitoring the surveillance program since September 2011.",
        "temperature": 1,
        "api_key": settings.ML_SERVICE_ENDPOINT_API_KEY,
        "length": 20,
        "top_k": 30,
    }

    endpoints = [
        # settings.GPT2_MEDIUM_API_ENDPOINT,
        settings.GPT2_LARGE_API_ENDPOINT,
        settings.GPT2_MEDIUM_HP_API_ENDPOINT,
        settings.GPT2_MEDIUM_LEGAL_API_ENDPOINT,
        settings.GPT2_MEDIUM_RESEARCH_API_ENDPOINT,
        settings.GPT2_MEDIUM_COMPANIES_API_ENDPOINT,
    ]

    for url in endpoints:
        response = requests.post(url, json=post_data)
        data = response.json()

        assert response.status_code == 200
        # make sure it returns text_4
        assert len(data["text_4"]) > 30
