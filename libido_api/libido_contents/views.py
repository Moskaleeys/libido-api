from rest_framework import status, viewsets, mixins
from django.shortcuts import render

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from oauth2_provider.contrib.rest_framework import (
    TokenHasReadWriteScope,
    TokenMatchesOASRequirements,
)
from libido_commons import permissions

from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from libido_rooms.models import Room, Category, RoomCategory
from libido_commons.paginations import CommonPagination
from libido_rooms.serializers import (
    RoomSerializer,
    RegisterRoomSerializer,
    CategorySerializer,
    # RoomCategorySerializer,
)
from libido_commons import renderers
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from libido_users.views import UserViewSet
from libido_users.models import User
from libido_contents.models import Content
from libido_contents.serializers import ContentSerializer


# Create your views here.


class ContentViewSet(
    mixins.ListModelMixin,  # retrive open -> user_id retrive
    mixins.RetrieveModelMixin,  # retrive open -> user_id retrive
    viewsets.GenericViewSet,
):
    __basic_fields = ("id", "title", "description", "url", "channel_title")
    permission_classes = [
        permissions.AllowRetriveList,
    ]
    renderer_classes = [renderers.LibidoApiJSONRenderer]
    queryset = Content.objects.all().exclude(deleted_at__isnull=False).order_by("-id")
    serializer_class = ContentSerializer
    pagination_class = CommonPagination
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filter_fields = __basic_fields
    search_fields = __basic_fields
