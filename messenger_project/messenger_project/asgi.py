import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from messenger_app.routing import websocket_urlpatterns
import socket

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messenger_project.settings')

# Динамически получаем свободный порт
def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 0))
        return s.getsockname()[1]

# Получаем свободный порт для WebSocket соединений
websocket_port = get_free_port()

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})

# Запускаем Daphne на свободном порту для WebSocket соединений
if __name__ == "__main__":
    import sys
    from django.core.management import execute_from_command_line

    # Проверяем, был ли указан порт в аргументах командной строки
    if len(sys.argv) > 1 and sys.argv[1] == "runserver":
        sys.argv[1] = f"runserver {websocket_port}"
    execute_from_command_line(sys.argv)
