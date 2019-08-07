import json
import logging

import aiohttp
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.core.cache import cache

from open.core.writeup.caches import get_cache_key_for_gpt2_parameter
from open.core.writeup.serializers import GPT2MediumPromptSerializer
from open.core.writeup.utilities.gpt2_serializers import serialize_gpt2_api_response

logger = logging.getLogger(__name__)


@database_sync_to_async
def get_cached_results(cache_key):
    return cache.get(cache_key)


@database_sync_to_async
def set_cached_results(cache_key, returned_data):
    cache.set(cache_key, returned_data)


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
        text_data_json = json.loads(text_data)
        serializer = GPT2MediumPromptSerializer(data=text_data_json)
        valid = serializer.is_valid()

        if not valid:
            return await self.return_invalid_data_prompt()

        prompt_serialized = serializer.validated_data

        cache_key = get_cache_key_for_gpt2_parameter(**prompt_serialized)
        cached_results = await get_cached_results(cache_key)

        if cached_results:
            return await self.send_serialized_data(cached_results)

        # switch auth styles, passing it here makes it a little bit more cross-operable
        # since aiohttp doesn't pass headers in the same way as the requests library
        # and you're too lazy to write custom middleware for one endpoint
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

        serialized_text_responses = serialize_gpt2_api_response(returned_data)
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
