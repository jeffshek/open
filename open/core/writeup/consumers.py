import json

import requests
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from django.conf import settings

from open.core.writeup.caches import get_cache_key_for_gpt2_parameter
from open.core.writeup.serializers import GPT2MediumPromptSerializer
from open.core.writeup.utilities import serialize_gpt2_responses
from django.core.cache import cache
import aiohttp


class WriteUpGPT2MediumConsumer(WebsocketConsumer):
    def connect(self):
        group_name = self.scope["url_route"]["kwargs"]["session_uuid"]
        self.group_name_uuid = "session_%s" % group_name

        async_to_sync(self.channel_layer.group_add)(
            self.group_name_uuid, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name_uuid, self.channel_name
        )

    def receive(self, text_data):
        print("sync")
        text_data_json = json.loads(text_data)

        serializer = GPT2MediumPromptSerializer(data=text_data_json)
        serializer.is_valid()
        prompt_serialized = serializer.validated_data

        cache_key = get_cache_key_for_gpt2_parameter(**prompt_serialized)
        cached_results = cache.get(cache_key)

        if cached_results:
            returned_data = cached_results
        else:
            token_key = f"Token {settings.ML_SERVICE_ENDPOINT_API_KEY}"
            headers = {"Authorization": token_key}
            response = requests.post(
                settings.GPT2_API_ENDPOINT, json=prompt_serialized, headers=headers
            )
            if response.status_code != 200:
                raise ValueError(f"Issue with {text_data_json}. Got {response.content}")

            # TODO - read more into this ... django's cache abstraction might actually make it work
            # without having to store in redis the proper way, xoxo django
            returned_data = response.json()
            cache.set(cache_key, returned_data)

        # make a copy of the response, but run a serialization process to clean
        # up any oddities like end of lines
        text_responses = returned_data.copy()

        for key, value in returned_data.items():
            if "text_" not in key:
                continue

            value_serialized = serialize_gpt2_responses(value)
            text_responses[key] = value_serialized

        async_to_sync(self.channel_layer.group_send)(
            self.group_name_uuid,
            {"type": "api_serialized_message", "message": text_responses},
        )

    def api_serialized_message(self, event):
        message = event["message"]

        self.send(text_data=json.dumps({"message": message}))


class WriteUpGPT2MediumConsumerMock(WriteUpGPT2MediumConsumer):
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        post_message = {"prompt": message}
        post_message["text_0"] = ". I am a test. That's wonderful."
        post_message["text_1"] = "Today, I saw potato in the fields."
        post_message["text_2"] = "! Our crops are growing."
        post_message["text_3"] = "How will we drink coffee tomorrow?"

        async_to_sync(self.channel_layer.group_send)(
            self.group_name_uuid,
            {"type": "api_serialized_message", "message": post_message},
        )


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

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        serializer = GPT2MediumPromptSerializer(data=text_data_json)
        serializer.is_valid()
        prompt_serialized = serializer.validated_data

        cache_key = get_cache_key_for_gpt2_parameter(**prompt_serialized)
        cached_results = await get_cached_results(cache_key)

        if cached_results:
            returned_data = cached_results
        else:
            token_key = f"Token {settings.ML_SERVICE_ENDPOINT_API_KEY}"
            headers = {"Authorization": token_key}

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    settings.GPT2_API_ENDPOINT, data=prompt_serialized, headers=headers
                ) as resp:
                    returned_data = await resp.json()

            await set_cached_results(cache_key, returned_data)

        text_responses = returned_data.copy()

        for key, value in returned_data.items():
            if "text_" not in key:
                continue

            value_serialized = serialize_gpt2_responses(value)
            text_responses[key] = value_serialized

        await self.channel_layer.group_send(
            self.group_name_uuid,
            {"type": "api_serialized_message", "message": text_responses},
        )

    async def api_serialized_message(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({"message": message}))
