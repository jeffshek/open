import asyncio
import json
import time
import uuid
import csv

import aiohttp

# from django.conf import settings
# import websockets


# this was mostly taken from a medium article ... it hasn't aged well and i should rewrite this.

# this script is used to ensure that load balancing works for the ML api endpoints
# python manage.py runscript swarm_ml_services

# urls = [settings.GPT2_MEDIUM_API_ENDPOINT] * 50000
# urls = ["wss://open.senrigan.io/ws/async/writeup/gpt2_medium/session/work/"] * 50


def get_urls(urls_to_create=50):
    urls = []

    for _ in range(urls_to_create):
        uuid_str = uuid.uuid4().__str__()
        ws_url = (
            f"wss://open.senrigan.io/ws/async/writeup/gpt2_medium/session/{uuid_str}/"
        )

        urls.append(ws_url)

    return urls


urls = get_urls(50000)


def get_random_prompt():
    import random
    from open.core.scripts.utilities import random_nouns

    random_word = random.choice(random_nouns)
    random_word_2 = random.choice(random_nouns)
    data = {
        "prompt": f"Today marks the day of {random_word}, I am eating {random_word}. Okay? {random_word_2}"
    }
    return data


async def fetch_url(session, url):
    data = {"prompt": f"Hello"}

    async with session.post(url, data=data, timeout=60 * 60) as response:
        if response.status != 200:
            error_text = await response.text()

            raise Exception(error_text)
        return await response.text()


count = 0


def increment_request_count():
    global count
    count += 1
    return count


async def fetch_all_urls(urls, loop):
    connector = aiohttp.TCPConnector(limit=100)

    async with aiohttp.ClientSession(connector=connector) as session:
        results = await asyncio.gather(
            # returning exceptions =  true means to ignore exceptions
            *[fetch_url(session, url) for url in urls],
            return_exceptions=False,
        )
        return results


async def fetch_via_websocket(session, url):
    ws = await session.ws_connect(url)

    print(increment_request_count())

    data = get_random_prompt()
    data_json = json.dumps(data)

    await ws.send_str(data_json)

    msg = await ws.receive()
    # msg = await asyncio.wait_for(ws.receive(), timeout=300.0)

    msg_json = msg.json()

    ws_msg_serialized = msg_json["message"]

    await ws.close()
    return ws_msg_serialized


async def fetch_all_urls_via_websockets(urls):
    connector = aiohttp.TCPConnector(limit=100)
    timeout = aiohttp.ClientTimeout(total=60 * 60)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:

        results = await asyncio.gather(
            # returning exceptions =  true means to ignore exceptions
            *[fetch_via_websocket(session, url) for url in urls],
            return_exceptions=True,
        )
        return results


def run():

    loop = asyncio.get_event_loop()

    start = time.time()
    data = loop.run_until_complete(fetch_all_urls_via_websockets(urls))
    end = time.time()

    with open("exports/output.csv", mode="w") as output:
        fieldnames = ["prompt", "text_0"]
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")

        writer.writeheader()

        for line in data:
            try:
                writer.writerow(line)
            except Exception:
                continue

    # a simple check to make sure we got all the data we wanted
    print(len(data))

    time_duration = end - start
    print(f"It took {time_duration} seconds to run.")
