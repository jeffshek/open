import asyncio
import json
import time
import uuid

import aiohttp

# from django.conf import settings
import websockets


# this was mostly taken from a medium article ... it hasn't aged well and i should rewrite this.

# this script is used to ensure that load balancing works for the ML api endpoints
# python manage.py runscript swarm_ml_services

# urls = [settings.GPT2_API_ENDPOINT] * 50000
# urls = ["wss://open.senrigan.io/ws/async/writeup/gpt2_medium/session/work/"] * 50


def get_urls(urls_to_create=50):
    urls = []

    for _ in range(urls_to_create):
        uuid_str = uuid.uuid4().__str__()
        ws_url = (
            f"wss://open.senrigan.io/ws/async/writeup/gpt2_medium/session/{uuid_str}/"
        )
        ws_url = f"ws://127.0.0.1:8008/ws/async/writeup/gpt2_medium/session/{uuid_str}/"

        urls.append(ws_url)
        # print (ws_url)

    return urls


urls = get_urls(5000)


exception_count = 0


def get_random_prompt():
    import random
    from open.core.scripts.utilities import random_nouns

    random_word = random.choice(random_nouns)
    data = {"prompt": f"Hello {random_word}, I am eating {random_word}."}
    return data


async def fetch_url(session, url):
    # random_word = random.choice(random_nouns)
    # data = {"prompt": f"Hello {random_word}, I am eating {random_word}."}

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


async def fetch_websocket_url(session, url):
    async with websockets.connect(url, ssl=True) as websocket:
        print(increment_request_count())

        data = get_random_prompt()
        data_json = json.dumps(data)

        await websocket.send(data_json)
        greeting = await websocket.recv()

        return greeting


async def fetch_all_urls(urls, loop):
    connector = aiohttp.TCPConnector(limit=100)

    async with aiohttp.ClientSession(connector=connector) as session:
        results = await asyncio.gather(
            # returning exceptions =  true means to ignore exceptions
            *[fetch_websocket_url(session, url) for url in urls],
            return_exceptions=False,
        )
        return results


def run():
    loop = asyncio.get_event_loop()

    start = time.time()
    htmls = loop.run_until_complete(fetch_all_urls(urls, loop))

    print(htmls[:50])
    end = time.time()

    # a simple check to make sure we got all the data we wanted
    print(len(htmls))

    time_duration = end - start
    print(f"It took {time_duration} seconds to run.")
