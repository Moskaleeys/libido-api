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
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True, help_text="방 설명")
    link_url = models.URLField(max_length=500)
    thumb = ProcessedImageField(
        blank=True,
        null=True,
        upload_to=upload_thumb,
        processors=[Thumbnail(150, 150)],
        format="JPEG",
        options={"quality": 90},
    )

    running_time = models.TimeField(null=True, blank=True, help_text="러닝타임")
    # view_count = models.PositiveIntegerField(null=True, default=0)
    # like_count = models.PositiveIntegerField(null=True)
    # dislike_count = models.PositiveIntegerField(null=True)
    channel_id = models.CharField(max_length=50, null=True)
    channel_title = models.CharField(max_length=50, null=True)
    published_at = models.CharField(max_length=50, null=True)

    # content_categories = models.ForeignKey(
    #     "ContentCategory", on_delete=models.CASCADE, related_name="contents"
    # )
    # content_tags = models.ManyToManyField(
    #     "Tag", through="ContentTag", related_name="contents"
    # )

    class Meta:
        verbose_name = "콘텐츠"
        verbose_name_plural = "콘텐츠 모음"
        db_table = "content"
        managed = True
