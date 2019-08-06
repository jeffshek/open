# flake8: noqa
import json
import time

import requests
from django.conf import settings
from websocket import create_connection

from open.core.scripts.swarm_ml_services import get_random_prompt

"""
this script's design was to compare performance behind django channels
and how much overhead it added versus directly hitting the microservice

output:

1.8620352506637574 was the average time in seconds to run.
1.8132854890823364 was the average time in seconds to run directly.

amazingly enough, django channels ... has almost zero overhead wow.
"""


def run():
    # dpy runscript writeup_profile_prompt_generate_view
    url = "wss://open.senrigan.io/ws/async/writeup/gpt2_medium/session/a-cool-test-session/"
    ws = create_connection(url)

    start = time.time()

    intervals = 50
    for _ in range(intervals):
        data = get_random_prompt()
        ws_msg = json.dumps(data)
        ws.send(ws_msg)
        result = ws.recv()

    end = time.time()

    websocket_difference = end - start
    print(f"{websocket_difference/intervals} was the average time in seconds to run.")

    url = settings.GPT2_API_ENDPOINT
    token_key = f"Token {settings.ML_SERVICE_ENDPOINT_API_KEY}"
    headers = {"Authorization": token_key}

    api_start = time.time()
    for _ in range(intervals):
        data = get_random_prompt()
        response = requests.post(url, json=data, headers=headers)
        assert response.status_code == 200

    api_end = time.time()

    api_difference = api_end - api_start
    print(
        f"{api_difference / intervals} was the average time in seconds to run directly."
    )
