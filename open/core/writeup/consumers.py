import json
import logging
from json import JSONDecodeError
from multiprocessing.dummy import Pool

import requests
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.core.cache import cache

from open.core.writeup.caches import (
    get_cache_key_for_text_algo_parameter,
    get_cache_key_for_processing_algo_parameter,
)
from open.core.writeup.constants import MLModelNames, WebsocketMessageTypes
from open.core.writeup.serializers import TextAlgorithmPromptSerializer
from open.core.writeup.utilities.text_algo_serializers import (
    serialize_text_algo_api_response,
    serialize_text_algo_api_response_sync,
)

# use a pool to run a post requests, otherwise it blocks
pool = Pool(10)
logger = logging.getLogger(__name__)


def on_post_success_to_microservice(response):
    if response.status_code != 200:
        return

    # after completion, we want to store the full results in a cache
    data = response.json()
    serialized = serialize_text_algo_api_response_sync(data)
    cache_key = data["cache_key"]
    cache.set(cache_key, serialized)


def on_error_to_microservice(ex):
    logger.exception(f"Post requests failed: {ex}")


@database_sync_to_async
def get_cached_results(cache_key):
    return cache.get(cache_key)


@database_sync_to_async
def set_cached_results(cache_key, returned_data):
    cache.set(cache_key, returned_data)


@database_sync_to_async
def check_if_cache_key_for_parameters_is_running(cache_key):
    is_cache_key_already_running = get_cache_key_for_processing_algo_parameter(
        cache_key
    )
    return cache.get(is_cache_key_already_running, False)


@database_sync_to_async
def set_request_flag_that_request_is_running_in_cache(cache_key):
    processing_cache_key = get_cache_key_for_processing_algo_parameter(cache_key)
    # set the cache to say this request is already running for 60 seconds
    # if it doesn't get the result by then, something is probably wrong
    cache.set(processing_cache_key, True, 60)


def get_api_endpoint_from_model_name(model_name):
    model_mapping_to_endpoints = {
        MLModelNames.GPT2_MEDIUM: settings.GPT2_MEDIUM_API_ENDPOINT,
        MLModelNames.GPT2_MEDIUM_LEGAL: settings.GPT2_MEDIUM_LEGAL_API_ENDPOINT,
        MLModelNames.GPT2_MEDIUM_HP: settings.GPT2_MEDIUM_HP_API_ENDPOINT,
        MLModelNames.GPT2_MEDIUM_RESEARCH: settings.GPT2_MEDIUM_RESEARCH_API_ENDPOINT,
        MLModelNames.GPT2_MEDIUM_COMPANIES: settings.GPT2_MEDIUM_COMPANIES_API_ENDPOINT,
        MLModelNames.GPT2_LARGE: settings.GPT2_LARGE_API_ENDPOINT,
        MLModelNames.XLNET_BASE_CASED: settings.XLNET_BASE_CASED_API_ENDPOINT,
        MLModelNames.XLNET_LARGE_CASED: settings.XLNET_LARGE_CASED_API_ENDPOINT,
        MLModelNames.TRANSFO_XL_WT103: settings.TRANSFORMERS_XL_API_ENDPOINT,
    }

    return model_mapping_to_endpoints[model_name]


class AsyncWriteUpGPT2MediumConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope["url_route"]["kwargs"]["session_uuid"]
        self.session_group_name_uuid = "session_%s" % self.group_name

        await self.channel_layer.group_add(
            self.session_group_name_uuid, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.session_group_name_uuid, self.channel_name
        )

    async def return_invalid_data_prompt(self, data):
        # make the prompt match back what was sent, this is used by the frontend
        # to validate what message is what
        error_msg = {
            "prompt": data.get("prompt", ""),
            "text_0": "Invalid Data Was Passed",
        }
        await self.channel_layer.group_send(
            self.session_group_name_uuid,
            {"type": "api_serialized_message", "message": error_msg},
        )

    async def return_invalid_api_response(self, prompt_serialized, resp, status, url):
        content = await resp.content.read()

        logger.exception(
            f"Issue with Request to ML Endpoint. Received {status} when accessing {url}. The data was {content}"
        )
        error_msg = {
            "prompt": prompt_serialized["prompt"],
            "text_0": "An Error Occurred",
        }
        return await self.channel_layer.group_send(
            self.session_group_name_uuid,
            {"type": "api_serialized_message", "message": error_msg},
        )

    async def post_to_microservice(self, url, prompt_serialized):
        """
        below is the multiple attempts of code, however aiohttp posts ends up as a blocking function ...
        this was so hard to diagnose, very frustrating.

        tbf - i still don't understand why aiohttp's ends up blocking the rest of django channels
        the reason it looks like httpx works is just because the timeout explodes so quickly

        async with aiohttp.ClientSession() as session:
        await session.post(url, data=prompt_serialized)

        async with aiohttp.ClientSession() as session:
            await self.fetch(url, data=prompt_serialized, session=session)


        ### another frustrating attempt with httpx, it sort of worked, but was ugly

        client = httpx.AsyncClient()
        try:
            await client.post(url, data=prompt_serialized)
        except Exception:
            # this post will timeout, but that's okay because it's a hack.
            # we don't really care about the message content from the post here, it takes too long to run
            # instead, we just need the service endpoints to have gotten the message and begin transmitting back
            # via the websocket channels the updated tokens
            pass
        finally:
            client.close()

        """
        # this is the only way that DOES not block django channels, whereas everything else did?!
        pool.apply_async(
            requests.post,
            args=[url, prompt_serialized],
            callback=on_post_success_to_microservice,
            error_callback=on_error_to_microservice,
        )

    async def _receive_new_request(self, data):
        """
        this function is kind of overwhelming (sorry), but what i'm doing is
        putting a few caches because running inference even with
        p100 gpus is still slow for transformer architectures

        the first cache checks if this request has been made before
        with the specific settings of word length, temp, etc

        the second cache sees if this request is already running,
        in most circumstances, that's overengineering, but some requests
        can take over ten seconds to run, so the worst case would be if
        it duplicated this request
        """
        serializer = TextAlgorithmPromptSerializer(data=data)

        # don't throw exceptions in the regular pattern raise_exception=True, all
        # exceptions need to be properly handled when using channels
        valid = serializer.is_valid()

        if not valid:
            return await self.return_invalid_data_prompt(data)

        prompt_serialized = serializer.validated_data

        cache_key = get_cache_key_for_text_algo_parameter(**prompt_serialized)
        cached_results = await get_cached_results(cache_key)
        if cached_results:
            return await self.send_serialized_data(cached_results)

        # technically a bug can probably occur if separate users try the same exact
        # phrase in the 180 seconds, but if that happens, that means the servers are probably
        # crushed from too many requests anyways, RIP
        duplicate_request = await check_if_cache_key_for_parameters_is_running(
            cache_key
        )
        if duplicate_request:
            print("Duplicate request already running.")
            return

        # if it doesnt' exist, add a state flag to say this is going to be running
        # so it will automatically broadcast back when if the frontend makes a duplicate request
        await set_request_flag_that_request_is_running_in_cache(cache_key)

        # switch auth styles, passing it here makes it a little bit more cross-operable
        # since aiohttp doesn't pass headers in the same way as the requests library
        # and you're too lazy to write custom middleware for one endpoint
        # the ml endpoints are protected via an api_key to prevent abuse
        prompt_serialized["api_key"] = settings.ML_SERVICE_ENDPOINT_API_KEY

        # pass the websocket_uuid for the ML endpoints to know how to communicate
        prompt_serialized["websocket_uuid"] = self.group_name
        prompt_serialized["cache_key"] = cache_key

        model_name = prompt_serialized["model_name"]
        url = get_api_endpoint_from_model_name(model_name)

        await self.post_to_microservice(url, prompt_serialized)

    async def _receive_updated_response(self, data):
        """ Send updates from a microservice back to the frontend """
        serialized_text_responses = await serialize_text_algo_api_response(data)
        await self.send_serialized_data(serialized_text_responses)

    async def receive(self, text_data):
        """

        TODO:
        - async/channels can only be tested with pytest, so configure pytest
        """
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json["message_type"]
        except JSONDecodeError as exc:
            logger.exception(f"Invalid JSON Error {exc}. Got {text_data}")
            return
        except KeyError as exc:
            logger.exception(f"Missing Message Type {exc} | {text_data}")
            return

        # use this as a routing channel that that will decipher if messages are coming
        # in from microservices or from the frontend
        if message_type == WebsocketMessageTypes.NEW_REQUEST:
            await self._receive_new_request(text_data_json)
        elif message_type in [
            WebsocketMessageTypes.UPDATED_RESPONSE,
            WebsocketMessageTypes.COMPLETED_RESPONSE,
        ]:
            await self._receive_updated_response(text_data_json)
        else:
            logger.exception(f"Invalid Message Type Received {message_type}")

    async def send_serialized_data(self, returned_data):
        await self.channel_layer.group_send(
            self.session_group_name_uuid,
            {"type": "api_serialized_message", "message": returned_data},
        )

    async def api_serialized_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))


class WriteUpGPT2MediumConsumerMock(AsyncWriteUpGPT2MediumConsumer):
    """
    This is a dummy endpoint I used for debugging, since it doesn't require
    having an active service architecture running.
    """

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["prompt"]

        post_message = {
            "prompt": message,
            "text_0": ". I am a test. That's wonderful.",
            "text_1": "Today, I saw potato in the fields.",
            "text_2": "! Our crops are growing.",
            "text_3": "How will we drink coffee tomorrow?",
        }

        await self.channel_layer.group_send(
            self.session_group_name_uuid,
            {"type": "api_serialized_message", "message": post_message},
        )
