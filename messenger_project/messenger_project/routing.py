from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from messenger_app.consumers import ChatConsumer

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/chats/<int:chat_id>/', ChatConsumer.as_asgi()),
    ]),
})
