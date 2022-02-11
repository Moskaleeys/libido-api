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


class Content(PrintableModel):
    title = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(max_length=550, blank=True, null=True, unique=True)
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
