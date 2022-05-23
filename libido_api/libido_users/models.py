from django.db import models
import smtplib
from email.mime.text import MIMEText
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

from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from django.core.validators import validate_email
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

    agree_marketing = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        help_text="마케팅 수신동의",
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

    country = CountryField(null=False, help_text="국가 필드", default="KR")

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
    def get_token(cls, user, app, duration, scope="read write"):
        uu_id = str(uuid.uuid1().hex)
        access_token = AccessToken.objects.create(
            user=user,
            scope=scope,
            expires=timezone.now() + timedelta(minutes=duration),
            token=uu_id,
            application=app,
        )

        return access_token.token

    @property
    def invitations(self):
        return self.invitation_receiver.filter(is_approved=False)

    @classmethod
    def is_exists(cls, username):
        return User.objects.filter(username=username).exists()

    @classmethod
    def tmp_token(cls, email, duration=60):
        try:
            Application = get_application_model()
            app = Application.objects.filter().first()
            user = cls.objects.get(username=email)
            access_token = cls.get_token(
                user=user, app=app, duration=duration, scope="read write tmp_token"
            )

        except Exception as e:
            print(e)
            raise exceptions.CreateTmpTokenError

        return access_token

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
    def check_nickname(cls, nickname):
        return cls.objects.filter(nickname=nickname).exists()

    @classmethod
    def check_userid(cls, userid):
        return cls.objects.filter(userid=userid).exists()

    @property
    def created_room_count(self):
        return self.room_moderator.count()

    @property
    def play_hours(self):
        return 3

    @property
    def play_minutes(self):
        return 3

    @property
    def room_cnt(self):
        return 3

    @property
    def friend_requests(self):
        return self.myfriend_friend.filter(is_approved=False)

    @property
    def friend_ids(self):
        return self.myfriend_user.filter(is_approved=True).values_list(
            "friend", flat=True
        )

    @property
    def friend_count(self):
        return self.myfriend_user.filter(is_approved=True).count()

    @property
    def genre(self):
        return "romance"

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
    def randoms(cls, user_id):
        my_friends = (
            cls.objects.filter(Q(user_id=user_id) | Q(friend_id=user_id))
            .filter(is_approved=True)
            .values_list("friend_id", flat=True)
        )
        return User.objects.filter(~Q(id__in=[my_friends])).exclude(id=user_id)

    @classmethod
    def approve(cls, request_friend_id, my_id):
        try:
            # 한쪽으로 추가 해주고, 반대쪽으로도 추가해준다
            myfriend = cls.objects.filter(
                user_id=request_friend_id,
                friend_id=my_id,
            ).update(is_approved=True)

            # 나 <-> 상대가 서로 요청을 한 상태의 경우 케이스
            cross_request, cross_request_is_exists = cls.objects.get_or_create(
                user_id=my_id, friend_id=request_friend_id, is_approved=True
            )
            return myfriend

        except Exception:
            return False

    @classmethod
    def decline(cls, user_id, friend_id):
        try:
            # 내쪽에서 삭제
            myfriend = cls.objects.filter(
                user_id=user_id,
                friend_id=friend_id,
            )
            myfriend.delete()

            # # 상대방 쪽에서 삭제
            # cross = cls.objects.filter(
            #     user_id=friend_id,
            #     friend_id=user_id,
            # )

            # cross.delete()

            return myfriend

        except Exception as e:
            print(e)
            return False

    @classmethod
    def connect(cls, user_id, friend_id):
        # exception 및 예외처리 구현 필요
        if user_id == friend_id:
            raise exceptions.InvalidFriendConenctError

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

            cross = cls.objects.filter(
                user_id=friend_id,
                friend_id=user_id,
            )
            cross.delete()

        except Exception:
            return False
        return True

    class Meta:
        verbose_name = "친구"
        verbose_name_plural = "친구 모음"
        db_table = "friend"
        managed = True
        constraints = [
            models.UniqueConstraint(
                fields=["user", "friend"], name="unique_status")
        ]


class EmailAuth(PrintableModel):
    target_email = models.CharField(null=True, blank=True, max_length=50)

    key = models.CharField(null=True, blank=True, max_length=50)

    is_confirmed = models.BooleanField(default=False)
    expired_at = models.DateTimeField(
        null=True, blank=True, db_index=True, default=None
    )
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(
        null=True,
        db_index=True,
        auto_now=True,
    )
    deleted_at = models.DateTimeField(
        null=True, blank=True, db_index=True, default=None
    )

    @classmethod
    def gen_number(cls, email):
        try:
            validate_email(email)
            assert User.objects.filter(username=email).exists() is True
            # 해당 엔드포인트에서
            # 무차별 대입 공격이 가능하기 때문에 꼭 Throttle 걸어야한다.
            nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
            random.shuffle(nums)
            auth_no = "".join(nums)[:8]
            email_auth = cls.objects.create(
                key=auth_no,
                target_email=email,
                is_confirmed=False,
                expired_at=timezone.now() + timedelta(minutes=8),
            )

            # email
            # cls.send_email_message(key=auth_no, email=email)
            cls.send_email_message_v0(key=auth_no, email=email)

            return email_auth

        except AssertionError as e:
            print(e)
            raise exceptions.InvalidEmailAddressError

        except ValidationError as e:
            print(e)
            raise exceptions.InvalidEmailAddressError

    @classmethod
    def send_email_message_v0(cls, key, email):
        smtp = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        smtp.starttls()
        smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        msg = MIMEText(
            f""" A 'Find your password' attempt requires further verification 
        because we did not recognize your device. 
        To complete the 'Find your password', enter the verification code on your new device

        Verification code: {key}
        """
        )

        msg["Subject"] = "Hi"

        smtp.sendmail(settings.EMAIL_HOST_USER, email, msg.as_string())
        smtp.quit()
        return True

    @classmethod
    def send_email_message(cls, key, email):
        email = EmailMessage(
            "Hi!",  # 제목
            f"""
            A 'Find your password' attempt requires further verification 
            because we did not recognize your device. 
            To complete the 'Find your password', enter the verification code on your new device

            Verification code: {key}

            """,
            f"{settings.EMAIL_HOST_USER}",
            to=[email],
        )
        email.send()
        return True

    @classmethod
    def confirm_number(cls, email, auth_key):
        try:
            mail = cls.objects.filter(
                key=auth_key,
                is_confirmed=False,
                target_email=email,
                expired_at__gte=timezone.now(),
            ).order_by("-id")[0]

            mail.is_confirmed = True
            mail.save()
        except Exception:

            raise exceptions.EmailAuthConfirmError

    def __str__(self):
        return "{}".format(self.key)

    class Meta:
        verbose_name = "이메일 인증"
        verbose_name_plural = "이메일 인증 모음"
        db_table = "email_auth"
        managed = True


class Invitation(PrintableModel):
    sender = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="invitation_sender",
        help_text="발송자",
    )
    receiver = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="invitation_receiver",
        help_text="수신자",
    )

    room = models.ForeignKey(
        "libido_rooms.Room",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="invitation_room",
        help_text="스트리밍 방",
    )

    is_approved = models.BooleanField(
        default=False,
        help_text="수락 상태",
    )

    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    deleted_at = models.DateTimeField(
        null=True, blank=True, db_index=True, default=None
    )

    @classmethod
    def decline(cls, sender_id, receiver_id):
        try:
            invitation = cls.objects.filter(
                sender=sender_id,
                receiver_id=receiver_id,
            )
            invitation.delete()
            return invitation

        except Exception:
            return False

    class Meta:
        verbose_name = "초대장"
        verbose_name_plural = "초대장 모음"
        db_table = "invitation"
        managed = True
