# messenger_app/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat, Message
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'

        # Присоединение к группе чата
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Отсоединение от группы чата
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        sender_id = data.get('sender_id')

        if message and sender_id:
            await self.save_message(sender_id, message)

            # Отправка сообщения всем участникам группы чата
            await self.channel_layer.group_send(
                self.chat_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender_id': sender_id,
                }
            )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']

        # Отправка сообщения клиенту
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
        }))

    @database_sync_to_async
    def save_message(self, sender_id, message):
        sender = User.objects.get(pk=sender_id)
        chat = Chat.objects.get(pk=self.chat_id)
        Message.objects.create(chat=chat, sender=sender, content=message)
