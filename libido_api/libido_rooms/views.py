from django.shortcuts import render
from rest_framework import status, viewsets, mixins
from libido_commons import permissions

from libido_rooms.models import Room, Category, RoomCategory
from libido_commons.paginations import CommonPagination
from libido_rooms.serializers import (
    RoomSerializer,
    CategorySerializer,
    # RoomCategorySerializer,
)
from libido_commons import renderers
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response


# Create your views here.


class RoomViewSet(
    mixins.ListModelMixin,  # retrive open -> user_id retrive
    mixins.RetrieveModelMixin,  # retrive open -> user_id retrive
    viewsets.GenericViewSet,
):
    __basic_fields = ("id", "title", "description", "category__name")
    permission_classes = [
        permissions.AllowRetriveList,
    ]
    renderer_classes = [renderers.LibidoApiJSONRenderer]
    queryset = Room.objects.all().exclude(deleted_at__isnull=False).order_by("-id")
    serializer_class = RoomSerializer
    pagination_class = CommonPagination
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filter_fields = __basic_fields
    search_fields = __basic_fields
