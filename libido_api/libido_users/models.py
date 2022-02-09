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


ISO3166 = {
    "AD": "Andorra",
    "AE": "United Arab Emirates",
    "AF": "Afghanistan",
    "AG": "Antigua & Barbuda",
    "AI": "Anguilla",
    "AL": "Albania",
    "AM": "Armenia",
    "AN": "Netherlands Antilles",
    "AO": "Angola",
    "AQ": "Antarctica",
    "AR": "Argentina",
    "AS": "American Samoa",
    "AT": "Austria",
    "AU": "Australia",
    "AW": "Aruba",
    "AZ": "Azerbaijan",
    "BA": "Bosnia and Herzegovina",
    "BB": "Barbados",
    "BD": "Bangladesh",
    "BE": "Belgium",
    "BF": "Burkina Faso",
    "BG": "Bulgaria",
    "BH": "Bahrain",
    "BI": "Burundi",
    "BJ": "Benin",
    "BM": "Bermuda",
    "BN": "Brunei Darussalam",
    "BO": "Bolivia",
    "BR": "Brazil",
    "BS": "Bahama",
    "BT": "Bhutan",
    "BU": "Burma (no longer exists)",
    "BV": "Bouvet Island",
    "BW": "Botswana",
    "BY": "Belarus",
    "BZ": "Belize",
    "CA": "Canada",
    "CC": "Cocos (Keeling) Islands",
    "CF": "Central African Republic",
    "CG": "Congo",
    "CH": "Switzerland",
    "CI": "Côte D'ivoire (Ivory Coast)",
    "CK": "Cook Iislands",
    "CL": "Chile",
    "CM": "Cameroon",
    "CN": "China",
    "CO": "Colombia",
    "CR": "Costa Rica",
    "CS": "Czechoslovakia (no longer exists)",
    "CU": "Cuba",
    "CV": "Cape Verde",
    "CX": "Christmas Island",
    "CY": "Cyprus",
    "CZ": "Czech Republic",
    "DD": "German Democratic Republic (no longer exists)",
    "DE": "Germany",
    "DJ": "Djibouti",
    "DK": "Denmark",
    "DM": "Dominica",
    "DO": "Dominican Republic",
    "DZ": "Algeria",
    "EC": "Ecuador",
    "EE": "Estonia",
    "EG": "Egypt",
    "EH": "Western Sahara",
    "ER": "Eritrea",
    "ES": "Spain",
    "ET": "Ethiopia",
    "FI": "Finland",
    "FJ": "Fiji",
    "FK": "Falkland Islands (Malvinas)",
    "FM": "Micronesia",
    "FO": "Faroe Islands",
    "FR": "France",
    "FX": "France, Metropolitan",
    "GA": "Gabon",
    "GB": "United Kingdom (Great Britain)",
    "GD": "Grenada",
    "GE": "Georgia",
    "GF": "French Guiana",
    "GH": "Ghana",
    "GI": "Gibraltar",
    "GL": "Greenland",
    "GM": "Gambia",
    "GN": "Guinea",
    "GP": "Guadeloupe",
    "GQ": "Equatorial Guinea",
    "GR": "Greece",
    "GS": "South Georgia and the South Sandwich Islands",
    "GT": "Guatemala",
    "GU": "Guam",
    "GW": "Guinea-Bissau",
    "GY": "Guyana",
    "HK": "Hong Kong",
    "HM": "Heard & McDonald Islands",
    "HN": "Honduras",
    "HR": "Croatia",
    "HT": "Haiti",
    "HU": "Hungary",
    "ID": "Indonesia",
    "IE": "Ireland",
    "IL": "Israel",
    "IN": "India",
    "IO": "British Indian Ocean Territory",
    "IQ": "Iraq",
    "IR": "Islamic Republic of Iran",
    "IS": "Iceland",
    "IT": "Italy",
    "JM": "Jamaica",
    "JO": "Jordan",
    "JP": "Japan",
    "KE": "Kenya",
    "KG": "Kyrgyzstan",
    "KH": "Cambodia",
    "KI": "Kiribati",
    "KM": "Comoros",
    "KN": "St. Kitts and Nevis",
    "KP": "Korea, Democratic People's Republic of",
    "KR": "Korea, Republic of",
    "KW": "Kuwait",
    "KY": "Cayman Islands",
    "KZ": "Kazakhstan",
    "LA": "Lao People's Democratic Republic",
    "LB": "Lebanon",
    "LC": "Saint Lucia",
    "LI": "Liechtenstein",
    "LK": "Sri Lanka",
    "LR": "Liberia",
    "LS": "Lesotho",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "LV": "Latvia",
    "LY": "Libyan Arab Jamahiriya",
    "MA": "Morocco",
    "MC": "Monaco",
    "MD": "Moldova, Republic of",
    "MG": "Madagascar",
    "MH": "Marshall Islands",
    "ML": "Mali",
    "MN": "Mongolia",
    "MM": "Myanmar",
    "MO": "Macau",
    "MP": "Northern Mariana Islands",
    "MQ": "Martinique",
    "MR": "Mauritania",
    "MS": "Monserrat",
    "MT": "Malta",
    "MU": "Mauritius",
    "MV": "Maldives",
    "MW": "Malawi",
    "MX": "Mexico",
    "MY": "Malaysia",
    "MZ": "Mozambique",
    "NA": "Namibia",
    "NC": "New Caledonia",
    "NE": "Niger",
    "NF": "Norfolk Island",
    "NG": "Nigeria",
    "NI": "Nicaragua",
    "NL": "Netherlands",
    "NO": "Norway",
    "NP": "Nepal",
    "NR": "Nauru",
    "NT": "Neutral Zone (no longer exists)",
    "NU": "Niue",
    "NZ": "New Zealand",
    "OM": "Oman",
    "PA": "Panama",
    "PE": "Peru",
    "PF": "French Polynesia",
    "PG": "Papua New Guinea",
    "PH": "Philippines",
    "PK": "Pakistan",
    "PL": "Poland",
    "PM": "St. Pierre & Miquelon",
    "PN": "Pitcairn",
    "PR": "Puerto Rico",
    "PT": "Portugal",
    "PW": "Palau",
    "PY": "Paraguay",
    "QA": "Qatar",
    "RE": "Réunion",
    "RO": "Romania",
    "RU": "Russian Federation",
    "RW": "Rwanda",
    "SA": "Saudi Arabia",
    "SB": "Solomon Islands",
    "SC": "Seychelles",
    "SD": "Sudan",
    "SE": "Sweden",
    "SG": "Singapore",
    "SH": "St. Helena",
    "SI": "Slovenia",
    "SJ": "Svalbard & Jan Mayen Islands",
    "SK": "Slovakia",
    "SL": "Sierra Leone",
    "SM": "San Marino",
    "SN": "Senegal",
    "SO": "Somalia",
    "SR": "Suriname",
    "ST": "Sao Tome & Principe",
    "SU": "Union of Soviet Socialist Republics (no longer exists)",
    "SV": "El Salvador",
    "SY": "Syrian Arab Republic",
    "SZ": "Swaziland",
    "TC": "Turks & Caicos Islands",
    "TD": "Chad",
    "TF": "French Southern Territories",
    "TG": "Togo",
    "TH": "Thailand",
    "TJ": "Tajikistan",
    "TK": "Tokelau",
    "TM": "Turkmenistan",
    "TN": "Tunisia",
    "TO": "Tonga",
    "TP": "East Timor",
    "TR": "Turkey",
    "TT": "Trinidad & Tobago",
    "TV": "Tuvalu",
    "TW": "Taiwan, Province of China",
    "TZ": "Tanzania, United Republic of",
    "UA": "Ukraine",
    "UG": "Uganda",
    "UM": "United States Minor Outlying Islands",
    "US": "United States of America",
    "UY": "Uruguay",
    "UZ": "Uzbekistan",
    "VA": "Vatican City State (Holy See)",
    "VC": "St. Vincent & the Grenadines",
    "VE": "Venezuela",
    "VG": "British Virgin Islands",
    "VI": "United States Virgin Islands",
    "VN": "Viet Nam",
    "VU": "Vanuatu",
    "WF": "Wallis & Futuna Islands",
    "WS": "Samoa",
    "YD": "Democratic Yemen (no longer exists)",
    "YE": "Yemen",
    "YT": "Mayotte",
    "YU": "Yugoslavia",
    "ZA": "South Africa",
    "ZM": "Zambia",
    "ZR": "Zaire",
    "ZW": "Zimbabwe",
    "ZZ": "Unknown or unspecified country",
}


class User(AbstractUser, PrintableModel):
    first_name = None
    last_name = None

    id = models.CharField(
        db_index=True,
        max_length=45,
        default=_generate_random_token,
        primary_key=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="활성화 상태",
        help_text="액티브된 유저 유무 확인 is_active 가 false로 된경우 accesstoken을 받아올 수 없다.",
    )

    nickname = models.CharField(
        verbose_name="외부 노출 닉네임",
        db_index=True,
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

    country = CountryField(null=True, blank=True, help_text="국가 필드")

    thumb = ProcessedImageField(
        blank=True,
        null=True,
        upload_to=upload_thumb,
        processors=[Thumbnail(150, 150)],
        format="JPEG",
        options={"quality": 90},
    )

    mobile = models.CharField(
        db_index=True,
        verbose_name="핸드폰 번호",
        max_length=50,
        blank=True,
        null=True,
        help_text="핸드폰 번호",
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

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자 모음"
        db_table = "user"
        managed = True


class MyFriend(PrintableModel):
    user = models.ForeignKey(
        get_user_model(),
        verbose_name="사용자",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="myfriend_user",
        help_text="유저",
    )

    friend = models.ForeignKey(
        get_user_model(),
        verbose_name="친구",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="myfriend_friend",
        help_text="친구",
    )

    is_approved = models.BooleanField(
        default=False,
        verbose_name="수락 상태",
        help_text="친구요청 수락 상태",
    )

    created_at = models.DateTimeField(
        verbose_name="친구초대 요청 시간",
        default=timezone.localtime,
        help_text="친구초대 요청시간",
    )

    def __str__(self):
        return f"{self.user} {self.friend}"

    @classmethod
    def approve(cls, user_id, friend_id):
        try:
            myfriend = cls.objects.filter(
                user_id=user_id,
                friend_id=friend_id,
            )
            myfriend.is_approved = True
            myfriend.save()

        except Exception:
            return False
        return True

    @classmethod
    def connect(cls, user_id, friend_id):
        # exception 및 예외처리 구현 필요
        myfriend, flag = cls.objects.get_or_create(
            user_id=user_id,
            friend_id=friend_id,
        )
        return myfriend

    @classmethod
    def disconnect(cls, user_id, friend_id):
        # exception 및 예외처리 구현 필요
        try:
            myfriend = cls.objects.filter(
                user_id=user_id,
                friend_id=friend_id,
            )
            myfriend.delete()
        except Exception:
            return False
        return True

    class Meta:
        verbose_name = "친구"
        verbose_name_plural = "친구 모음"
        db_table = "friend"
        managed = True
        constraints = [
            models.UniqueConstraint(fields=["user", "friend"], name="unique_status")
        ]
