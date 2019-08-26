# flake8: noqa
import requests
from django.conf import settings

from open.core.writeup.utilities.text_algo_serializers import (
    serialize_text_algo_api_response
)

"""
dpy runscript writeup_debug_end_of_text_not_serialized
"""


def run():
    data = {
        "prompt": "We know that this is an important moment in the history of our country he said. We are proud to support the work of the American Civil Liberties Union and we will continue to fight for the rights of all Americans. The ACLU is currently suing the government over its surveillance programs. The ACLU said it had been monitoring the surveillance program since September 2011.",
        "temperature": 1,
        "api_key": settings.ML_SERVICE_ENDPOINT_API_KEY,
        "length": 20,
        "top_k": 30,
    }

    response = requests.post(settings.GPT2_MEDIUM_API_ENDPOINT, data=data)
    returned_data = response.json()
    serialized_text_responses = serialize_text_algo_api_response(returned_data)
