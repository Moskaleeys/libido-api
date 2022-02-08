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

from django.conf import settings
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

# Create your models here.


def upload_img(instance, filename):
    user_id = instance.id
    _ts = int(time.time())
    _, ext = os.path.splitext(filename)
    return f"users/{user_id}/img/{_ts}{ext}"


def upload_thumb(instance, filename):
    user_id = instance.id
    _ts = int(time.time())
    _, ext = os.path.splitext(filename)
    return f"users/{user_id}/thumb/{_ts}{ext}"


class User(AbstractUser, PrintableModel):
    first_name = None
    last_name = None

    id = models.CharField(
        db_index=True,
        max_length=40,
        default=_generate_random_token,
        primary_key=True,
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="활성화 상태",
        help_text="액티브된 유저 유무 확인 is_active 가 false로 된경우 accesstoken을 받아올 수 없다.",
    )

    nickname = models.CharField(
        verbose_name="외부 노출 닉네임",
        max_length=50,
        blank=True,
        null=True,
        help_text="외부 노출되는 이름(닉네임)",
    )

    date_of_birth = models.DateField(blank=True, null=True, help_text="생일")

    bio = models.TextField(
        verbose_name=_("Bio"),
        max_length=3000,
        blank=True,
        null=True,
        default=None,
        help_text="자기소개",
    )

    thumb = ProcessedImageField(
        blank=True,
        null=True,
        upload_to=upload_thumb,
        processors=[Thumbnail(150, 150)],
        format="JPEG",
        options={"quality": 90},
    )

    mobile = models.CharField(
        verbose_name="핸드폰 번호", max_length=50, blank=True, null=True, help_text="핸드폰 번호"
    )

    last_login = models.DateTimeField(
        verbose_name="최근 로그인 한 시간", default=timezone.now, help_text="가장 최근 로그인 한 시간"
    )

    created_at = models.DateTimeField(
        verbose_name="가입 한 날짜 및 시간",
        db_index=True,
        default=timezone.now,
        help_text="유저를 최초 가입 또는 생성한 시간",
    )

    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"), null=True, auto_now=True, db_index=True
    )

    deleted_at = models.DateTimeField(
        verbose_name="탈퇴 또는 삭제한 시간",
        null=True,
        default=None,
        blank=True,
        db_index=True,
        help_text="탈퇴 또는 삭제한 시간",
    )

    objects = UserManager()

    @classmethod
    def is_exists(cls, username):
        return User.objects.filter(username=username).exists()

    @property
    def thumb_url(self):
        try:
            if self.thumb:
                return self.thumb.url
            else:
                return None

        except Exception:
            return None

    @classmethod
    def check_username(cls, username):
        return cls.objects.filter(username=username).exists()

    @classmethod
    def check_userid(cls, userid):
        return cls.objects.filter(userid=userid).exists()

    def __str__(self):
        return f"{self.username} {self.nickname}"

    def __repr__(self):
        return f"{self.username} {self.nickname}"

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자 모음"
        db_table = "user"
        managed = True
