from django.conf.urls import include, url
from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from libido_rooms.views import (
    RoomViewSet,
    FriendsRoomViewSet,
    UserRoomViewSet,
)
from libido_users.urls import user_router


default_router = DefaultRouter(trailing_slash=False)
default_router.register(r"rooms", RoomViewSet, basename="rooms")
default_router.register(r"friend_rooms", FriendsRoomViewSet, basename="friends_rooms")

user_room_router = NestedSimpleRouter(
    user_router, "users", lookup="users", trailing_slash=False
)

user_room_router.register(
    r"rooms",
    UserRoomViewSet,
    basename="user-room-viewset",
)

urlpatterns = [
    url(r"^", include(default_router.urls)),
    url(r"^", include(user_room_router.urls)),
]
