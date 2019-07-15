from channels.generic.websocket import AsyncWebsocketConsumer, JsonWebsocketConsumer
import json
from asgiref.sync import async_to_sync


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))


class WriteUpSessionConsumer(JsonWebsocketConsumer):
    def connect(self):
        group_name = self.scope["url_route"]["kwargs"]["session_uuid"]
        self.group_name_uuid = "session_%s" % group_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name_uuid, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name_uuid, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name_uuid, {"type": "chat_message", "message": message}
        )

    def chat_message(self, event):
        message = event["message"]

        self.send(text_data=json.dumps({"message": message}))
