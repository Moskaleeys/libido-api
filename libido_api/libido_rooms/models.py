from django.db import models
import datetime
from datetime import timedelta
from enum import IntEnum
from io import BytesIO
import json
import os
import random
import secrets
import sys
import time
import uuid

from django_countries.fields import CountryField
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from django.core.validators import validate_email
from django.db import transaction
from django.db.models import Count, Sum
from django.db.models import Q
from django.db.utils import IntegrityError
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from oauth2_provider.models import AccessToken, RefreshToken, get_application_model
import requests
from rest_framework import status
from social_django.models import UserSocialAuth

from libido_commons import exceptions
from libido_commons.models import PrintableModel
from libido_commons.utils import _generate_random_token


class ThingRoomType(models.IntegerChoices):
    PERSONAL = 0, "스트리밍"
    BUSINESS = 1, "녹화"


class Category(PrintableModel):
    name = models.CharField(
        db_index=True,
        max_length=50,
        help_text="카테고리 이름",
        unique=True,
    )

    created_at = models.DateTimeField(
        verbose_name="Created at", db_index=True, default=timezone.now
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "카테고리"
        verbose_name_plural = "카테고리 모음"
        db_table = "category"
        managed = True


class Room(PrintableModel):
    id = models.CharField(
        db_index=True,
        max_length=45,
        default=_generate_random_token,
        primary_key=True,
    )

    moderator = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
        related_name="room_moderator",
        help_text="방장(모더레이터)",
    )

    title = models.CharField(
        db_index=True, max_length=100, null=True, blank=True, help_text="타이틀"
    )
    description = models.TextField(null=True, blank=True, help_text="방 설명")
    is_public = models.BooleanField(db_index=True, default=True, help_text="공개방 여부")
    password = models.CharField(blank=True, null=True, max_length=250, help_text="비밀번호")
    user_count = models.PositiveIntegerField(
        null=True, blank=True, default=0, help_text="접속한 사람수"
    )

    category = models.ManyToManyField(
        "libido_rooms.Category",
        through="libido_rooms.RoomCategory",
        blank=True,
        help_text="룸 카테고리들",
    )

    contents = models.ManyToManyField(
        "libido_contents.Content",
        through="libido_rooms.RoomContent",
        blank=True,
        help_text="룸 콘텐츠",
    )

    created_at = models.DateTimeField(db_index=True, default=timezone.now)

    deleted_at = models.DateTimeField(
        null=True,
        default=None,
        blank=True,
        db_index=True,
        help_text="탈퇴 또는 삭제한 시간",
    )

    class Meta:
        verbose_name = "방"
        verbose_name_plural = "방 모음"
        db_table = "room"
        managed = True


class RoomCategory(PrintableModel):
    category = models.ForeignKey(
        "libido_rooms.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="roomcategory_category",
        help_text="카테고리",
    )

    room = models.ForeignKey(
        "libido_rooms.Room",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="roomcategory_room",
        help_text="스트리밍 방",
    )

    created_at = models.DateTimeField(db_index=True, default=timezone.now)

    def __str__(self):
        return f"{self.id} {self.category} {self.room}"

    class Meta:
        verbose_name = "방 카테고리"
        verbose_name_plural = "방 카테고리 모음"
        db_table = "room_category"
        managed = True

        constraints = [
            models.UniqueConstraint(
                fields=["category", "room"], name="unique_category_room"
            )
        ]


class RoomContent(PrintableModel):
    content = models.ForeignKey(
        "libido_contents.Content",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="roomcontent_content",
        help_text="콘텐츠",
    )

    room = models.ForeignKey(
        "libido_rooms.Room",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="roomcontent_room",
        help_text="스트리밍 방",
    )

    created_at = models.DateTimeField(db_index=True, default=timezone.now)

    def __str__(self):
        return f"{self.id} {self.category} {self.room}"

    class Meta:
        verbose_name = "방 콘텐츠"
        verbose_name_plural = "방 콘텐츠 모음"
        db_table = "room_content"
        managed = True

        constraints = [
            models.UniqueConstraint(
                fields=["content", "room"], name="unique_content_room"
            )
        ]
