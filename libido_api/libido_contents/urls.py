from django.conf.urls import include, url
from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from libido_contents.views import (
    ContentViewSet,
)
from libido_users.urls import user_router


default_router = DefaultRouter(trailing_slash=False)
default_router.register(r"contents", ContentViewSet, basename="rooms")

urlpatterns = [
    url(r"^", include(default_router.urls)),
]
