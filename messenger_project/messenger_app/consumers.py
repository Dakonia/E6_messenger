# # messenger_app/consumers.py
#
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import Chat
#
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.chat_id = self.scope['url_route']['kwargs']['chat_id']
#         await self.channel_layer.group_add(
#             f'chat_{self.chat_id}',
#             self.channel_name
#         )
#
#         # Получение списка участников чата по chat_id
#         chat = Chat.objects.get(pk=self.chat_id)
#         participants = chat.participants.all()
#
#
#         # Отправка списка участников на клиентскую сторону
#         await self.send(text_data=json.dumps({
#             'participants': [user.username for user in participants]
#         }))
#
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             f'chat_{self.chat_id}',
#             self.channel_name
#         )
#
#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['text']
#         await self.channel_layer.group_send(
#             f'chat_{self.chat_id}',
#             {
#                 'type': 'chat_message',
#                 'sender': 'Me',
#                 'message': message,
#             }
#         )
#
#     async def chat_message(self, event):
#         sender = event['sender']
#         message = event['message']
#         print(f"Sending message: {message}")
#         await self.send(text_data=json.dumps({
#             'sender': sender,
#             'message': message,
#         }))

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        await self.channel_layer.group_add(
            f'chat_{self.chat_id}',
            self.channel_name
        )
        await self.accept()
# Проблема в этом поле
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f'chat_{self.chat_id}',
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['text']
        await self.channel_layer.group_send(
            f'chat_{self.chat_id}',
            {
                'type': 'chat_message',
                'sender': 'Me',
                'message': message,
            }
        )

    async def chat_message(self, event):
        sender = event['sender']
        message = event['message']
        await self.send(text_data=json.dumps({
            'sender': sender,
            'message': message,
        }))
