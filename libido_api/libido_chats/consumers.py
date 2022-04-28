import json
import logging

from asgiref.sync import sync_to_async
from django.contrib.auth import authenticate, get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer, JsonWebsocketConsumer

from libido_chats.models import Message
from libido_rooms.models import Room

from libido_commons import exceptions


request_logger = logging.getLogger("default")


class KeepUserConsumerMixin:
    channel_session = True
    # @staticmethod
    # def _save_user(func):
    #     def wrapper(message, **kwargs):
    #         if message.user is not None and message.user.is_authenticated():
    #             message.channel_session["user_id"] = message.user.id
    #         return func(message, **kwargs)
    #     return wrapper

    @staticmethod
    def _save_user(func):
        def wrapper(message, *args, **kwargs):
            if message.user is not None and message.user.is_authenticated():
                message.channel_session["user_id"] = message.user.id
            return func(message, *args, **kwargs)

        return wrapper

    def __getattribute__(self, name):
        method = super().__getattribute__(name)
        if name == "connect":
            return self._save_user(method)
        return method

    @property
    def user(self):
        if not hasattr(self, "_user"):
            user_id = self.message.channel_session["user_id"]
            self._user = get_user_model().objects.get(id=user_id)
        return self._user


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        request_logger.info(self.__dict__)
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = "chat_%s" % self.room_id

        # Join room
        # 처음 이부분에서 조인함
        # 방은 이부분에서 만들면 절대로 안되지만,,
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # import ipdb
        # ipdb.set_trace()

        # create room
        # await self.create_room(room_id=self.room_id)

        # get room
        await self.get_room(room_id=self.room_id)

    async def disconnect(self, close_code):
        # Leave room
        request_logger.info(self.__dict__)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from web socket
    async def receive(self, text_data):
        print(text_data)
        data = json.loads(text_data)
        print(data)
        message = data["message"]
        nickname = data["nickname"]
        username = data.get("username", "empty")
        room_id = data["room"]

        request_logger.info(
            {
                "message": message,
                "nickname": nickname,
                "type": "chat_message",
                "username": username,
            }
        )
        await self.save_message(nickname=nickname, room_id=room_id, message=message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "nickname": nickname,
                "username": username,
            },
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        nickname = event["nickname"]
        username = event.get("username", "empty")

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {"message": message, "nickname": nickname, "username": username}
            )
        )

    @sync_to_async
    def create_room(self, room_id):
        Room.objects.get_or_create(id=room_id)

    @sync_to_async
    def get_room(self, room_id):
        try:
            Room.objects.get(id=room_id)
        except Exception:
            raise exceptions.RoomDoesNotExists

    @sync_to_async
    def save_message(self, nickname, room_id, message, username="empty"):
        Message.objects.create(
            nickname=nickname, room_id=room_id, content=message, username=username
        )
