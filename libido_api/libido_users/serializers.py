import bcrypt
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import BCryptSHA256PasswordHasher, make_password
from django.db import transaction
from rest_framework import serializers
from social_django.models import UserSocialAuth

from libido_users.models import User, MyFriend, Invitation


class UserStatSerializer(serializers.Serializer):
    play_time = serializers.ReadOnlyField(source="play_time", allow_null=True)
    create_room_cnt = serializers.ReadOnlyField(
        source="create_room_cnt", allow_null=True
    )
    genre = serializers.ReadOnlyField(source="genre", allow_null=True)
    friend_cnt = serializers.ReadOnlyField(source="friend_cnt", allow_null=True)


class UserSerializer(serializers.ModelSerializer):
    is_social_login = serializers.ReadOnlyField()
    social_login_provider = serializers.ReadOnlyField()
    created_room_count = serializers.ReadOnlyField(allow_null=True)
    friend_count = serializers.ReadOnlyField(allow_null=True)
    genre = serializers.ReadOnlyField(allow_null=True)

    class Meta:
        model = User
        fields = "__all__"

    def validate_password(self, value, hasher=BCryptSHA256PasswordHasher.algorithm):
        return make_password(value, salt=bcrypt.gensalt(11), hasher=hasher)


class UserLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "thumb", "nickname"]


class RegisterSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField(label="이메일(유저네임)")
    password = serializers.CharField(label="비밀번호")
    country = serializers.CharField(label="국가코드")
    mobile = serializers.CharField(label="핸드폰번호")
    nickname = serializers.CharField(label="닉네임")

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("username is exists")
        else:
            return value

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            mobile=validated_data["mobile"],
            nickname=validated_data["nickname"],
            country=validated_data["country"],
            password=make_password(
                validated_data["password"],
                salt=bcrypt.gensalt(11),
                hasher=BCryptSHA256PasswordHasher.algorithm,
            ),
            is_active=True,
        )

        return user


class SendInvitationSerializer(serializers.Serializer):
    receiver_ids = serializers.ListField(
        child=serializers.CharField(),
        required=True,
        help_text="유저 아이디들",
        label="유저 아이디들",
        write_only=True,
    )

    room_id = serializers.CharField(required=True, label="스트리밍 방 pk", write_only=True)

    def create(self, validated_data):
        receiver_ids = validated_data.get("receiver_ids")
        room_id = validated_data.get("room_id")
        sender = getattr(self.context["request"], "user")
        bulk_arr = []
        for receiver_id in receiver_ids:
            bulk_arr.append(
                Invitation(
                    sender=sender,
                    room_id=room_id,
                    receiver_id=receiver_id,
                )
            )
        result = Invitation.objects.bulk_create(bulk_arr)
        # 대충 첫번째꺼만 리턴
        return result[:1]


class MyFriendSerializer(serializers.ModelSerializer):
    friend_nickname = serializers.ReadOnlyField(
        source="friend.nickname", allow_null=True
    )
    friend_thumb_url = serializers.ReadOnlyField(
        source="friend.thumb_url", allow_null=True
    )
    friend_email = serializers.ReadOnlyField(source="friend.username", allow_null=True)

    class Meta:
        fields = "__all__"
        model = MyFriend


class InvitationSerializer(serializers.ModelSerializer):
    sender = UserLightSerializer(allow_null=True)
    receiver = UserLightSerializer(allow_null=True)

    class Meta:
        fields = "__all__"
        model = Invitation
