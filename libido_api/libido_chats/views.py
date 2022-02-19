from django.shortcuts import render
from libido_commons.paginations import CommonPagination, CommonCursorPagination
from rest_framework import status, viewsets, mixins
from libido_chats.models import Message
from libido_chats.serializers import MessageSerializer

from libido_commons import renderers
from libido_commons import permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from oauth2_provider.contrib.rest_framework import (
    TokenHasReadWriteScope,
)


class ServiceBaseViewSet(
    mixins.ListModelMixin,  # retrive open -> user_id retrive
    mixins.RetrieveModelMixin,  # retrive open -> user_id retrive
    viewsets.GenericViewSet,
):
    pass


def index(request):
    # no need auth ?
    return render(request, "libido_chats/index.html")


def room(request, room_id):
    # check oauth2 ?
    nickname = request.GET.get("nickname", "Anonymous")
    messages = Message.objects.filter(room_id=room_id)[0:25]

    return render(
        request,
        "libido_chats/room.html",
        {"room_id": room_id, "nickname": nickname, "messages": messages},
    )


class MessageViewSet(ServiceBaseViewSet):
    __basic_fields = ("id", "nickname", "created_at")
    permission_classes = [
        permissions.AllowRetriveList,
        TokenHasReadWriteScope,
    ]
    renderer_classes = [renderers.LibidoApiJSONRenderer]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = CommonCursorPagination
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filter_fields = __basic_fields
    search_fields = __basic_fields

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        qs = queryset.filter(nickname=user.nickname).order_by("-id")
        return qs
