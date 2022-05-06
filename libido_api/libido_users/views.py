from email.policy import HTTP
from django.contrib.auth import get_user_model
from django.core.cache import cache
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from oauth2_provider.contrib.rest_framework import (
    TokenHasReadWriteScope,
    TokenMatchesOASRequirements,
)
from oauth2_provider.models import AccessToken, get_application_model
from rest_framework import status, viewsets
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from libido_commons import exceptions
from libido_commons import renderers
from libido_commons.mixins import DeleteMixin
from libido_commons.paginations import CommonPagination
from libido_commons.permissions import NoCreate, NoDelete, NoRetrive
from libido_users.models import User, MyFriend, EmailAuth, Invitation
from libido_users.serializers import (
    RegisterSerializer,
    SendInvitationSerializer,
    InvitationSerializer,
    UserSerializer,
    MyFriendSerializer,
    FriendRequestSerializer,
)


class BaseViewSet(
    # mixins.CreateModelMixin,
    mixins.ListModelMixin,  # retrive open -> user_id retrive
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
        operation_summary="아이디 중복 검사",
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

    @action(methods=["PUT"], detail=False, url_path="thumb", permission_classes=[])
    def update_thumb(self, request, *args, **kwargs):
        userId = request.user.id
        target = User.objects.get(id=userId)
        target.thumb = request.data["thumb"]
        target.save()
        return Response(request.user.username, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="post",
        operation_summary="유저 통계",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={},
        ),
    )
    @action(methods=["POST"], detail=False, url_path="stats", permission_classes=[])
    def stats(self, request):
        user = request.user
        result = {
            "play_time": user.play_minutes,
            "room_cnt": user.room_cnt,
            "genre": user.genre,
            "friends": user.friend_count,
        }
        return Response(result, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="post",
        operation_summary="내가 받은 초대장들",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={},
        ),
    )
    @action(
        methods=["POST"], detail=False, url_path="invitations", permission_classes=[]
    )
    def invitations(self, request):
        user = request.user
        serializer = InvitationSerializer(
            instance=user.invitations, many=True, allow_null=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="post",
        operation_summary="내가 받은 친구초대들",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={},
        ),
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="friend_requests",
        permission_classes=[],
    )
    def friend_requests(self, request):
        user = request.user
        serializer = FriendRequestSerializer(
            instance=user.friend_requests, many=True, allow_null=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="post",
        operation_summary="닉네임 중복 검사",
        operation_description="닉네임 중복검사 엔드포인트",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "nickname": openapi.Schema(
                    type=openapi.TYPE_STRING, description="유저네임(이메일주소)"
                ),
            },
        ),
    )
    @action(
        methods=["POST"], detail=False, url_path="check_nickname", permission_classes=[]
    )
    def check_nickname(self, request):
        nickname = request.data["nickname"]
        is_duplicate = User.check_nickname(nickname=nickname)
        return Response({"is_duplicate": is_duplicate}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="post",
        operation_summary="비밀번호 찾기 키값 검증 엔드포인트",
        operation_description="비밀번호 찾기 이메일 확인 엔드포인트 - 리턴값으로 비밀번호 변경에 필요한 토큰 리턴",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
                "auth_key": openapi.Schema(type=openapi.TYPE_STRING, description="인증키"),
            },
        ),
    )
    @action(
        methods=["post"],
        detail=False,
        url_path="confirm_email_auth",
        permission_classes=[],
    )
    def confirm_email_auth(self, request):
        # 인엑티브 이메일이 된경우 # email 그리고 임시 pw를 받는다
        # 그 다음 임시 토큰을 만들어서 프론트에 주도록 한다.
        # 해당 토큰 유호 시간은 5분으로 정한다.
        # 꼭 어세스 토큰만 발급을 해주고, 리프래시는 주지않는다.
        email = self.request.data.get("username", None)
        auth_key = self.request.data.get("auth_key", None)

        if not email:
            raise exceptions.EmailAuthConfirmError

        if not auth_key:
            raise exceptions.EmailAuthConfirmError

        EmailAuth.confirm_number(email=email, auth_key=auth_key)

        token = User.tmp_token(email=email)
        return Response({"access_token": token}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="post",
        operation_summary="비밀번호 찾기용 인증메일발송",
        operation_description="비밀번호찾기용 인증메일발송",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
            },
        ),
    )
    @action(
        methods=["post"],
        detail=False,
        permission_classes=[],
    )
    def send_email_auth(self, request):
        try:
            email = request.data.get("username")
            EmailAuth.gen_number(email=email)
            return Response({"results": True}, status=status.HTTP_200_OK)

        except AssertionError:
            raise exceptions.ParameterError

        except exceptions.InvalidEmailAddressError as e:
            print(e)
            raise exceptions.InvalidEmailAddressError

        except Exception as e:
            print(e)
            return Response({"data": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method="post",
        operation_summary="등록한 핸드폰번호 확인",
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

    @swagger_auto_schema(
        operation_summary="이메일 회원가입 ",
        request_body=RegisterSerializer,
        responses={201: RegisterSerializer},
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
        operation_summary="회원탈퇴",
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
    __basic_fields = ("id", "user", "friend", "is_approved", "created_at")
    parent = UserViewSet
    parent_object = User
    parent_lookup_field = "user"
    lookup_field = "user"
    queryset = MyFriend.objects.filter().order_by("-id")
    permission_classes = [TokenHasReadWriteScope]
    renderer_classes = [renderers.LibidoApiJSONRenderer]
    pagination_class = CommonPagination
    serializer_action_classes = {
        "list": MyFriendSerializer,
        "send_invitation": SendInvitationSerializer,
    }

    filter_fields = __basic_fields
    search_fields = __basic_fields

    # def get_queryset(self):
    #     if isinstance(self.request.user, User):
    #         qs = super().get_queryset().filter(users=self.request.user).order_by("-id")
    #         return qs
    #     qs = super().get_queryset().order_by("-id")
    #     return qs

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        qs = (
            queryset.select_related("user")
            .filter(user=user)
            .filter(is_approved=True)
            .order_by("-id")
        )
        return qs

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except KeyError:
            return MyFriendSerializer

    @swagger_auto_schema(
        operation_summary="스트리밍 초대장 발송",
        request_body=SendInvitationSerializer,
        # responses={201: RoomSerializer},
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="send_invitation",
        permission_classes=[TokenHasReadWriteScope],
    )
    def send_invitation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="post",
        operation_summary="초대장 거절 ",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "sender_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="보낸사람 유저 아이디"
                ),
            },
        ),
        responses={status.HTTP_200_OK: MyFriendSerializer},
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="decline_invitation",
        permission_classes=[TokenHasReadWriteScope],
    )
    def decline_invitation(self, request, *args, **kwargs):
        user = request.user
        sender_id = request.data["sender_id"]
        Invitation.decline(sender_id=sender_id, receiver_id=user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        method="post",
        operation_summary="친구요청 수락",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "friend_id": openapi.Schema(
                    type=openapi.TYPE_STRING, description="친구요청 수락할 친구 PK"
                ),
            },
        ),
        responses={status.HTTP_200_OK: MyFriendSerializer},
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="approve",
        permission_classes=[TokenHasReadWriteScope],
    )
    def approve(self, request, *args, **kwargs):
        request_friend_id = request.data["friend_id"]
        my_id = request.user.id
        friend = MyFriend.approve(
            request_friend_id=request_friend_id, my_id=my_id)
        serializers = MyFriendSerializer(instance=friend, allow_null=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="post",
        operation_summary="친구요청 거절 ",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "friend_id": openapi.Schema(
                    type=openapi.TYPE_STRING, description="친구요청 거절 friend_id"
                ),
            },
        ),
        responses={status.HTTP_200_OK: MyFriendSerializer},
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="decline",
        permission_classes=[TokenHasReadWriteScope],
    )
    def decline(self, request, *args, **kwargs):
        friend_id = request.data["friend_id"]
        user_id = request.user.id
        friend = MyFriend.decline(user_id=user_id, friend_id=friend_id)
        serializers = MyFriendSerializer(instance=friend, allow_null=True)
        return Response(serializers.data, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        method="post",
        operation_summary="친구요청 신청",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "friend_id": openapi.Schema(
                    type=openapi.TYPE_STRING, description="친구 맺을 유저 PK"
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
    def connect(self, request, *args, **kwargs):
        friend_id = request.data["friend_id"]
        user_id = request.user.id
        follow = MyFriend.connect(user_id=user_id, friend_id=friend_id)
        serializers = MyFriendSerializer(instance=follow, allow_null=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="post",
        operation_summary="친구요청 랜덤친구 찾기",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={},
        ),
        responses={status.HTTP_200_OK: MyFriendSerializer},
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="randoms",
        permission_classes=[TokenHasReadWriteScope],
    )
    def randoms(self, request, *args, **kwargs):
        user_id = request.user.id
        randomic = MyFriend.randoms(user_id=user_id)
        serializers = UserSerializer(
            instance=randomic, allow_null=True, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="post",
        operation_summary="친구삭제",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "friend_id": openapi.Schema(
                    type=openapi.TYPE_STRING, description="친구 삭제할 유저 PK"
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
    def disconnect(self, request, *args, **kwargs):
        friend_id = request.data["friend_id"]
        user_id = request.user.id
        MyFriend.disconnect(user_id=user_id, friend_id=friend_id)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        method="post",
        operation_summary="단일 친구의 스트리밍방",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "friend_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="친구 유저 PK"
                ),
            },
        ),
        responses={status.HTTP_200_OK: MyFriendSerializer},
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="rooms",
        permission_classes=[TokenHasReadWriteScope],
    )
    def rooms(self, request, *args, **kwargs):
        from libido_rooms.models import Room
        from libido_rooms.serializers import RoomSerializer

        friend_id = request.data["friend_id"]
        rooms = Room.objects.filter(moderator_id=friend_id)
        serializers = RoomSerializer(
            instance=rooms, many=True, allow_null=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
