from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .models import Message, ChatRoom


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)

        username = data.get("username", "Anonymous")
        message = data.get("message", "")

        room, created = ChatRoom.objects.get_or_create(
            name=self.room_name
        )

        Message.objects.create(
            room=room,
            username=username,
            content=message
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": text_data,
            }
        )

    def chat_message(self, event):
        data = json.loads(event["message"])

        self.send(
            text_data=f"{data['username']}: {data['message']}"
        )     