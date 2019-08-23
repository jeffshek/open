import json
import logging

import aiohttp
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.core.cache import cache

from open.core.writeup.caches import (
    get_cache_key_for_text_algo_parameter,
    get_cache_key_for_processing_algo_parameter,
)
from open.core.writeup.constants import MLModelNames
from open.core.writeup.serializers import TextAlgorithmPromptSerializer
from open.core.writeup.utilities.text_algo_serializers import (
    serialize_text_algo_api_response
)

logger = logging.getLogger(__name__)


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
def set_if_request_is_running_in_cache(cache_key):
    is_cache_key_already_running = get_cache_key_for_processing_algo_parameter(
        cache_key
    )
    # set the cache to say this request is already running for 180 seconds
    # if it doesn't get the result by then, something is probably wrong
    cache.set(is_cache_key_already_running, True, 180)


def get_api_endpoint_from_model_name(model_name):
    model_mapping_to_endpoints = {
        MLModelNames.GPT2_MEDIUM: settings.GPT2_API_ENDPOINT,
        MLModelNames.XLNET_BASE_CASED: settings.XLNET_BASE_CASED_API_ENDPOINT,
        MLModelNames.XLNET_LARGE_CASED: settings.XLNET_LARGE_CASED_API_ENDPOINT,
        MLModelNames.TRANSFO_XL_WT103: settings.TRANSFORMERS_XL_API_ENDPOINT,
    }

    # default to gpt2 for now until you feel confident
    url = model_mapping_to_endpoints.get(model_name, settings.GPT2_API_ENDPOINT)
    return url


class AsyncWriteUpGPT2MediumConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        group_name = self.scope["url_route"]["kwargs"]["session_uuid"]
        self.group_name_uuid = "session_%s" % group_name

        await self.channel_layer.group_add(self.group_name_uuid, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name_uuid, self.channel_name)

    async def return_invalid_data_prompt(self):
        error_msg = {
            "prompt": "Invalid Data Was Passed",
            "text_0": "Invalid Data Was Passed",
        }
        await self.channel_layer.group_send(
            self.group_name_uuid,
            {"type": "api_serialized_message", "message": error_msg},
        )

    async def return_invalid_api_response(self, prompt_serialized, status, url):
        logger.exception(
            f"Issue with Request to ML Endpoint. Received {status} when accessing {url}",
            exec_info=True,
        )
        error_msg = {
            "prompt": prompt_serialized["prompt"],
            "text_0": "An Error Occurred",
        }
        return await self.channel_layer.group_send(
            self.group_name_uuid,
            {"type": "api_serialized_message", "message": error_msg},
        )

    async def receive(self, text_data):
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

        TODO:
        - async/channels can only be tested with pytest, so configure pytest
        """

        text_data_json = json.loads(text_data)
        serializer = TextAlgorithmPromptSerializer(data=text_data_json)

        # don't throw exceptions in the regular pattern raise_exception=True, all
        # exceptions need to be properly handled
        valid = serializer.is_valid()

        if not valid:
            return await self.return_invalid_data_prompt()

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
            return

        # if it doesnt' exist, add a state flag to say this is going to be running
        # so it will automatically broadcast back when if the frontend makes a duplicate request
        await set_if_request_is_running_in_cache(cache_key)

        # switch auth styles, passing it here makes it a little bit more cross-operable
        # since aiohttp doesn't pass headers in the same way as the requests library
        # and you're too lazy to write custom middleware for one endpoint
        # the ml endpoints are protected via an api_key to prevent abuse
        prompt_serialized["api_key"] = settings.ML_SERVICE_ENDPOINT_API_KEY

        model_name = prompt_serialized["model_name"]
        url = get_api_endpoint_from_model_name(model_name)

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=prompt_serialized) as resp:
                status = resp.status

                # if the ml endpoints are hit too hard, we'll receive a 500 error
                if resp.status != 200:
                    return await self.return_invalid_api_response(
                        prompt_serialized, status, url
                    )

                returned_data = await resp.json()

        serialized_text_responses = serialize_text_algo_api_response(returned_data)
        await set_cached_results(cache_key, serialized_text_responses)

        await self.send_serialized_data(returned_data)

    async def send_serialized_data(self, returned_data):
        await self.channel_layer.group_send(
            self.group_name_uuid,
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

        post_message = {"prompt": message}
        post_message["text_0"] = ". I am a test. That's wonderful."
        post_message["text_1"] = "Today, I saw potato in the fields."
        post_message["text_2"] = "! Our crops are growing."
        post_message["text_3"] = "How will we drink coffee tomorrow?"

        await self.channel_layer.group_send(
            self.group_name_uuid,
            {"type": "api_serialized_message", "message": post_message},
        )
