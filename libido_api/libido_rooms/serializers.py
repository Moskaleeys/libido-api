import bcrypt
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import BCryptSHA256PasswordHasher, make_password
from django.db import transaction
from rest_framework import serializers
from libido_rooms.models import Room, Category, RoomCategory
from libido_contents.models import Content
from libido_contents.serializers import ContentSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, allow_null=True)
    contents = ContentSerializer(many=True, allow_null=True)

    class Meta:
        model = Room
        fields = "__all__"
