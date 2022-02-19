from django.urls import path
from django.conf.urls import include, url

from libido_chats import views
from libido_rooms.urls import default_router as rooms_router

from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter


message_router = NestedSimpleRouter(
    rooms_router, "rooms", lookup="rooms", trailing_slash=False
)
message_router.register(
    r"messages",
    views.MessageViewSet,
    basename="messages-viewset",
)

urlpatterns = [
    path("demo/chat", views.index, name="index"),
    path("demo/rooms/<str:room_id>/", views.room, name="room"),
    url(r"^", include(message_router.urls)),
]
