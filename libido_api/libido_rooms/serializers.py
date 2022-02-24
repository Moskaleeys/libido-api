import bcrypt
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import BCryptSHA256PasswordHasher, make_password
from django.db import transaction
from rest_framework import serializers
from django.contrib.auth.models import AnonymousUser
from libido_commons import exceptions
from libido_users.serializers import UserSerializer
from libido_rooms.models import Room, Category, RoomCategory, RoomUser
from libido_contents.models import Content
from libido_contents.serializers import ContentSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, allow_null=True)
    contents = ContentSerializer(many=True, allow_null=True)
    users = UserSerializer(many=True, allow_null=True)

    class Meta:
        model = Room
        fields = "__all__"


class RegisterRoomSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(required=True, help_text="타이틀", label="타이틀")
    description = serializers.CharField(required=True, help_text="설명", label="설명")
    password = serializers.CharField(
        help_text="비밀번호",
        label="비밀번호",
        required=False,
        allow_null=True,
        allow_blank=True,
    )

    content_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=0),
        required=True,
        help_text="콘텐츠 아이디값들",
        label="콘텐츠 아이디값들",
        write_only=True,
    )

    def create(self, validated_data):
        request = self.context.get("request")
        if isinstance(request.user, AnonymousUser):
            return exceptions.CreateUserLinkError

        user = request.user
        title = validated_data.get("title", None)
        description = validated_data.get("description", None)
        password = validated_data.get("password", None)
        content_ids = validated_data.get("content_ids", None)

        if (password is None) or (password is ""):
            is_public = True
            password = None
        else:
            is_public = False
            # make password
            password = Room.set_password(pw=password)

        contents_query = Content.objects.filter(id__in=content_ids)
        play_lists_count = contents_query.count()
        room = Room.objects.create(
            moderator=user,
            title=title,
            play_lists_count=play_lists_count,
            description=description,
            is_public=is_public,
            password=password,
        )
        room.contents.add(*contents_query)
        return room
