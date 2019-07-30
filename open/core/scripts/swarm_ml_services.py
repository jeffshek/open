import asyncio
import time

import aiohttp
from django.conf import settings

import random

# this script is used to ensure that load balancing works for the ML api endpoints
# python manage.py runscript swarm_ml_services

# this was mostly taken from a medium article ... it hasn't aged well and i should rewrite this.
from open.core.scripts.utilities import random_nouns

urls = [settings.GPT2_API_ENDPOINT] * 500


async def fetch_url(session, url):
    random_word = random.choice(random_nouns)

    data = {"prompt": f"Hello {random_word}, I am eating {random_word}."}

    async with session.post(url, data=data, timeout=60 * 60) as response:
        return await response.text()


async def fetch_all_urls(urls, loop):
    connector = aiohttp.TCPConnector(limit=100)

    async with aiohttp.ClientSession(connector=connector) as session:
        results = await asyncio.gather(
            *[fetch_url(session, url) for url in urls], return_exceptions=True
        )
        return results


def run():
    loop = asyncio.get_event_loop()

    start = time.time()
    htmls = loop.run_until_complete(fetch_all_urls(urls, loop))
    # print (htmls)

    print(htmls[:50])
    end = time.time()

    # a simple check to make sure we got all the data we wanted
    print(len(htmls))

    time_duration = end - start
    print(f"It took {time_duration} seconds to run.")
