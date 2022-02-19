from django.urls import path

from libido_chats import consumers

websocket_urlpatterns = [
    path("ws/<str:room_id>/", consumers.ChatConsumer.as_asgi()),
]
