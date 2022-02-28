from rest_framework import status, viewsets, mixins
from django.shortcuts import render

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from oauth2_provider.contrib.rest_framework import (
    TokenHasReadWriteScope,
    TokenMatchesOASRequirements,
)
from libido_commons import permissions
from libido_commons.filters import MinMaxRoomFilter

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


# Create your views here.


class RoomViewSet(
    mixins.ListModelMixin,  # retrive open -> user_id retrive
    mixins.RetrieveModelMixin,  # retrive open -> user_id retrive
    viewsets.GenericViewSet,
):
    __basic_fields = (
        "id",
        "title",
        "description",
        "category__name",
        "play_lists_count",
        "moderator__username",
        "moderator__email",
        "moderator__id",
        "min_user_count",
        "max_user_count",
        "min_play_lists_count",
        "max_play_lists_count",
    )
    permission_classes = [
        permissions.AllowRetriveList,
    ]
    renderer_classes = [renderers.LibidoApiJSONRenderer]
    queryset = Room.objects.all().exclude(deleted_at__isnull=False).order_by("?")
    serializer_class = RoomSerializer
    pagination_class = CommonPagination
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_class = MinMaxRoomFilter
    filter_fields = __basic_fields
    search_fields = [
        "id",
        "title",
        "description",
        "category__name",
        "moderator__email",
        "moderator__username",
    ]
    ordering_fields = __basic_fields


class FriendsRoomViewSet(
    mixins.ListModelMixin,  # retrive open -> user_id retrive
    mixins.RetrieveModelMixin,  # retrive open -> user_id retrive
    viewsets.GenericViewSet,
):
    __basic_fields = (
        "id",
        "title",
        "description",
        "category__name",
        "play_lists_count",
        "moderator__username",
        "moderator__email",
        "moderator__id",
        "min_user_count",
        "max_user_count",
        "min_play_lists_count",
        "max_play_lists_count",
    )
    permission_classes = [
        TokenHasReadWriteScope,
        permissions.AllowRetriveList,
    ]
    renderer_classes = [renderers.LibidoApiJSONRenderer]
    queryset = Room.objects.all().exclude(deleted_at__isnull=False).order_by("?")
    serializer_class = RoomSerializer
    pagination_class = CommonPagination
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_class = MinMaxRoomFilter
    filter_fields = __basic_fields
    search_fields = __basic_fields
    ordering_fields = __basic_fields

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        qs = (
            queryset.select_related("moderator")
            .filter(moderator__id__in=[user.friend_ids])
            .order_by("-id")
        )
        return qs


class UserRoomViewSet(viewsets.ModelViewSet):
    __basic_fields = ("id", "moderator", "title")
    parent = UserViewSet
    renderer_classes = [renderers.LibidoApiJSONRenderer]
    parent_object = User
    parent_lookup_field = "user"
    permission_classes = [
        TokenHasReadWriteScope,
    ]

    queryset = Room.objects.all()

    serializer_class = RoomSerializer
    pagination_class = CommonPagination
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    filter_fields = __basic_fields
    search_fields = __basic_fields
    ordering_fields = __basic_fields

    serializer_action_classes = {
        "list": RoomSerializer,
        "create": RegisterRoomSerializer,
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        qs = queryset.select_related("moderator").filter(moderator=user).order_by("-id")
        return qs

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except KeyError:
            return RoomSerializer

    @swagger_auto_schema(
        operation_summary="방 만들기",
        request_body=RegisterRoomSerializer,
        responses={201: RoomSerializer},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        method="post",
        operation_summary="방 비밀번호 확인",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="방 비밀번호"
                ),
            },
        ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"result": openapi.Schema(type=openapi.TYPE_OBJECT)},
            ),
        },
    )
    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[TokenHasReadWriteScope],
    )
    def check_password(self, request, *args, **kwargs):
        password = request.data.get("password", None)
        room = Room.get_room(pk=kwargs["pk"])
        result = room.check_password(pw=password)
        return Response({"result": result}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="post",
        operation_summary="방참여",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="방 비밀번호"
                ),
            },
        ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"result": openapi.Schema(type=openapi.TYPE_OBJECT)},
            ),
        },
    )
    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[TokenHasReadWriteScope],
    )
    def join(self, request, *args, **kwargs):
        user_id = request.user.id
        password = request.data.get("password", None)
        room_id = kwargs["pk"]
        room = Room.join(room_id=room_id, password=password, user_id=user_id)
        serializer = RoomSerializer(instance=room)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="post",
        operation_summary="방 나가기",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={},
        ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"result": openapi.Schema(type=openapi.TYPE_OBJECT)},
            ),
        },
    )
    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[TokenHasReadWriteScope],
    )
    def leave(self, request, *args, **kwargs):
        user_id = request.user.id
        room_id = kwargs["pk"]
        room = Room.leave(room_id=room_id, user_id=user_id)
        serializer = RoomSerializer(instance=room)
        return Response(serializer.data, status=status.HTTP_200_OK)
