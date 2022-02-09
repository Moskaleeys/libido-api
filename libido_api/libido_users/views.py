from django.contrib.auth import get_user_model
from django.core.cache import cache
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from oauth2_provider.contrib.rest_framework import (
    TokenHasReadWriteScope,
    TokenMatchesOASRequirements,
)
from oauth2_provider.models import AccessToken, get_application_model
from rest_framework import status, viewsets
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from libido_commons import exceptions
from libido_commons import renderers
from libido_commons.mixins import DeleteMixin
from libido_commons.paginations import CommonPagination
from libido_commons.permissions import NoCreate, NoDelete, NoRetrive
from libido_users.models import User, MyFriend
from libido_users.serializers import (
    RegisterSerializer,
    UserSerializer,
    MyFriendSerializer,
)


class BaseViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,  # retrive open -> user_id retrive
    # mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class UserViewSet(DeleteMixin, BaseViewSet):
    queryset = User.objects.all()
    permission_classes = [
        NoCreate,
        NoDelete,
        TokenHasReadWriteScope,
        TokenMatchesOASRequirements,
    ]
    renderer_classes = [renderers.LibidoApiJSONRenderer]
    required_alternate_scopes = {
        "GET": [["read"]],
        # 실질적으로 해당 scope 토큰은 존재하지않음
        "POST": [["signup_token"]],
        "PATCH": [["write"]],
        "PUT": [["write"]],
        "DELETE": [["delete_token"]],
    }

    serializer_action_classes = {
        "list": UserSerializer,
        "me": UserSerializer,
        "create": RegisterSerializer,
        "sign_up": RegisterSerializer,
        "update": UserSerializer,
        "partial_update": UserSerializer,
    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except KeyError:
            return UserSerializer

    @swagger_auto_schema(
        method="post",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING, description="유저네임(이메일주소)"
                ),
            },
        ),
    )
    @action(
        methods=["POST"], detail=False, url_path="check_username", permission_classes=[]
    )
    def check_username(self, request):
        username = request.data["username"]
        is_duplicate = User.check_username(username=username)
        return Response({"is_duplicate": is_duplicate}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="post",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "mobile": openapi.Schema(type=openapi.TYPE_STRING, description="핸드폰번호"),
            },
        ),
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="is_registered_mobile",
        permission_classes=[],
    )
    def is_registered_mobile(self, request):
        mobile = request.data["mobile"]
        is_registered = User.is_registered_mobile(mobile=mobile)
        return Response(
            {"is_registered_number": is_registered}, status=status.HTTP_200_OK
        )

    @action(methods=["POST"], detail=False, url_path="sign_up", permission_classes=[])
    def sign_up(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["GET"], detail=False, url_path="me")
    def get_me(self, request):
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="post",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={},
        ),
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="withdrawal",
        permission_classes=[TokenHasReadWriteScope],
    )
    def withdrawal(self, request):
        User.withdrawal(user_id=self.request.user.id)
        return Response({"result": True}, status=status.HTTP_200_OK)

    @get_me.mapping.patch
    def patch_me(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(res.data, status=status.HTTP_200_OK)

    def list(self, request):
        result = UserSerializer(instance=request.user)
        return Response(result.data, status=status.HTTP_200_OK)


class MyFriendViewSet(BaseViewSet):
    __basic_fields = ("id", "user", "friend", "is_approved", "created_at", "deleted_at")

    queryset = MyFriend.objects.all().order_by("-id")
    permission_classes = [TokenHasReadWriteScope]
    renderer_classes = [renderers.LibidoApiJSONRenderer]
    pagination_class = CommonPagination
    serializer_action_classes = {
        "list": MyFriendSerializer,
    }

    filter_fields = __basic_fields
    search_fields = __basic_fields

    def get_queryset(self):
        if isinstance(self.request.user, User):
            qs = super().get_queryset().filter(users=self.request.user).order_by("-id")
            return qs
        qs = super().get_queryset().order_by("-id")
        return qs

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except KeyError:
            return UserSerializer

    @swagger_auto_schema(
        method="post",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "friend_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="친구요청 수락할 친구 PK"
                ),
            },
        ),
        responses={status.HTTP_200_OK: MyFriendSerializer},
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="connect",
        permission_classes=[TokenHasReadWriteScope],
    )
    def approve(self, request):
        friend_id = request.data["friend_id"]
        user_id = request.user.id
        follow = MyFriend.approve(user_id=user_id, friend_id=friend_id)
        serializers = MyFriendSerializer(instance=follow, allow_null=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="post",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "friend_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="친구 맺을 유저 PK"
                ),
            },
        ),
        responses={status.HTTP_200_OK: MyFriendSerializer},
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="connect",
        permission_classes=[TokenHasReadWriteScope],
    )
    def connect(self, request):
        friend_id = request.data["friend_id"]
        user_id = request.user.id
        follow = MyFriend.connect(user_id=user_id, friend_id=friend_id)
        serializers = MyFriendSerializer(instance=follow, allow_null=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="post",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "friend_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="친구 삭제할 유저 PK"
                ),
            },
        ),
        responses={status.HTTP_200_OK: MyFriendSerializer},
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="disconnect",
        permission_classes=[TokenHasReadWriteScope],
    )
    def disconnect(self, request):
        friend_id = request.data["friend_id"]
        user_id = request.user.id
        MyFriend.disconnect(user_id=user_id, friend_id=friend_id)
        return Response(None, status=status.HTTP_204_NO_CONTENT)
