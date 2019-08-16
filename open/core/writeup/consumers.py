import json
import logging

import aiohttp
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.core.cache import cache

from open.core.writeup.caches import (
    get_cache_key_for_text_algo_parameter,
    get_cache_key_for_processing_gpt2_parameter,
)
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
def check_if_cache_key_for_gpt2_parameter_is_running(cache_key):
    is_cache_key_already_running = get_cache_key_for_processing_gpt2_parameter(
        cache_key
    )
    return cache.get(is_cache_key_already_running, False)


@database_sync_to_async
def set_if_request_is_running_in_cache(cache_key):
    is_cache_key_already_running = get_cache_key_for_processing_gpt2_parameter(
        cache_key
    )
    # set the cache to say this request is already running for 180 seconds
    # if it doesn't get the result by then, something is probably wrong
    cache.set(is_cache_key_already_running, True, 180)


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

    async def return_invalid_api_response(self, prompt_serialized, status):
        logger.exception(f"Issue with Request to ML Endpoint. Received {status}")
        error_msg = {
            "prompt": prompt_serialized["prompt"],
            "text_0": "An Error Occurred",
        }
        return await self.channel_layer.group_send(
            self.group_name_uuid,
            {"type": "api_serialized_message", "message": error_msg},
        )

    async def receive(self, text_data):
        # TODO - async/Channels can only be tested with pytest
        # so i need to configure pytest and then ... test

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
        duplicate_request = await check_if_cache_key_for_gpt2_parameter_is_running(
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

        async with aiohttp.ClientSession() as session:
            async with session.post(
                settings.GPT2_API_ENDPOINT, data=prompt_serialized
            ) as resp:
                status = resp.status

                # if the ml endpoints are hit too hard, we'll receive a 500 error
                if resp.status != 200:
                    return await self.return_invalid_api_response(
                        prompt_serialized, status
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
