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


def upload_thumb(instance, filename):
    content_id = instance.id
    _ts = int(time.time())
    _, ext = os.path.splitext(filename)
    return f"contents/{content_id}/thumb/{_ts}{ext}"


class Genre(PrintableModel):
    name = models.CharField(
        db_index=True,
        max_length=50,
        help_text="장르 이름",
        unique=True,
    )

    created_at = models.DateTimeField(
        verbose_name="Created at", db_index=True, default=timezone.now
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "장르"
        verbose_name_plural = "장르 모음"
        db_table = "genre"
        managed = True


class Content(PrintableModel):
    title = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(max_length=254, blank=True, null=True, unique=True)
    description = models.TextField(null=True, blank=True, help_text="방 설명")
    thumb_url = models.URLField(max_length=500, blank=True, null=True)
    channel_id = models.CharField(max_length=50, null=True, blank=True)
    channel_title = models.CharField(max_length=50, null=True, blank=True)
    thumb = ProcessedImageField(
        blank=True,
        null=True,
        upload_to=upload_thumb,
        processors=[Thumbnail(350, 350)],
        format="JPEG",
        options={"quality": 90},
    )

    genre = models.ManyToManyField(
        "libido_contents.Genre",
        through="libido_contents.ContentGenre",
        blank=True,
        help_text="콘텐츠 장르",
    )

    view_count = models.PositiveIntegerField(null=True, default=0, blank=True)
    like_count = models.PositiveIntegerField(null=True, default=0, blank=True)
    dislike_count = models.PositiveIntegerField(null=True, default=0, blank=True)

    running_time = models.TimeField(null=True, blank=True, help_text="러닝타임")
    published_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(db_index=True, default=timezone.now)

    deleted_at = models.DateTimeField(
        null=True,
        default=None,
        blank=True,
        db_index=True,
        help_text="삭제한 시간",
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "콘텐츠"
        verbose_name_plural = "콘텐츠 모음"
        db_table = "content"
        managed = True


class ContentGenre(PrintableModel):
    genre = models.ForeignKey(
        "libido_contents.Genre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contentgenre_genre",
        help_text="장르",
    )

    content = models.ForeignKey(
        "libido_contents.Content",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contentgenre_content",
        help_text="콘텐츠",
    )

    created_at = models.DateTimeField(db_index=True, default=timezone.now)

    def __str__(self):
        return f"{self.id} {self.genre}"

    class Meta:
        verbose_name = "콘텐츠 장르"
        verbose_name_plural = "콘텐츠 장르 모음"
        db_table = "content_genre"
        managed = True

        constraints = [
            models.UniqueConstraint(
                fields=["content", "genre"], name="unique_content_genre"
            )
        ]


class UserContentHistory(PrintableModel):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
        related_name="usercontenthistory_user",
        help_text="유저",
    )

    minute = models.PositiveIntegerField(
        null=True, default=0, blank=True, help_text="시청 분"
    )
    genre = models.CharField(max_length=20, blank=True, null=True, help_text="장르")

    content = models.ForeignKey(
        "libido_contents.Content",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="usercontenthistoy_content",
        help_text="콘텐츠",
    )

    created_at = models.DateTimeField(db_index=True, default=timezone.now)

    class Meta:
        verbose_name = "사용자 콘텐츠 시청기록"
        verbose_name_plural = "사용자 콘텐츠 시청기록 모음"
        db_table = "user_content_history"
        managed = True
