from django.conf.urls import include, url
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from libido_users.views import UserViewSet, MyFriendViewSet

user_router = DefaultRouter(trailing_slash=False)
user_router.register(r"users", UserViewSet, basename="users")

myfriend_router = NestedSimpleRouter(
    user_router, "users", lookup="users", trailing_slash=False
)

myfriend_router.register(
    r"friends",
    MyFriendViewSet,
    basename="myfriends",
)


urlpatterns = [
    url(r"^", include(user_router.urls)),
    url(r"^", include(myfriend_router.urls)),
]
