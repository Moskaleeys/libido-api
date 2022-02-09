import bcrypt
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import BCryptSHA256PasswordHasher, make_password
from django.db import transaction
from rest_framework import serializers
from social_django.models import UserSocialAuth

from libido_users.models import User


class UserSerializer(serializers.ModelSerializer):
    is_social_login = serializers.ReadOnlyField()
    social_login_provider = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = "__all__"

    def validate_password(self, value, hasher=BCryptSHA256PasswordHasher.algorithm):
        return make_password(value, salt=bcrypt.gensalt(11), hasher=hasher)


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
