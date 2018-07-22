# chat/routing.py
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<room_name>/', consumers.ChatConsumer, name='ws_chat_room'),
]
