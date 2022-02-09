from django.db import models
from django.utils import timezone

from libido_commons.models import PrintableModel

# Create your models here.
class AppVersion(PrintableModel):
    os = models.CharField(
        verbose_name="운영체제", null=True, blank=True, max_length=15, help_text="운영체"
    )

    current_version = models.CharField(
        verbose_name="현재 앱 버전", null=True, blank=True, max_length=15, help_text="현재 버전"
    )

    min_version = models.CharField(
        verbose_name="최소 버전", null=True, blank=True, max_length=15, help_text="최소 버전"
    )

    created_at = models.DateTimeField(db_index=True, default=timezone.localtime)

    updated_at = models.DateTimeField(
        null=True,
        auto_now=True,
    )
    deleted_at = models.DateTimeField(
        null=True, blank=True, default=None, db_index=True
    )

    def __str__(self):
        return f"{self.os}"

    class Meta:
        verbose_name = "앱 버전"
        verbose_name_plural = "앱 버전 모음"
        db_table = "app_version"
        managed = True


class TermsOfService(PrintableModel):
    title = models.CharField(null=True, blank=True, max_length=300, help_text="타이틀")

    content = models.TextField(
        max_length=50000,
        blank=True,
        null=True,
        default=None,
        help_text="콘텐츠",
    )

    created_at = models.DateTimeField(db_index=True, default=timezone.now)

    updated_at = models.DateTimeField(
        null=True,
        auto_now=True,
    )
    deleted_at = models.DateTimeField(
        null=True, blank=True, default=None, db_index=True
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "이용 약관"
        verbose_name_plural = "이용 약관 모음"
        db_table = "terms_of_service"
        managed = True


class PrivacyPolicy(PrintableModel):
    title = models.CharField(null=True, blank=True, max_length=300, help_text="타이틀")

    content = models.TextField(
        max_length=50000,
        blank=True,
        null=True,
        default=None,
        help_text="콘텐츠",
    )

    created_at = models.DateTimeField(db_index=True, default=timezone.now)

    updated_at = models.DateTimeField(
        null=True,
        auto_now=True,
    )
    deleted_at = models.DateTimeField(
        null=True, blank=True, default=None, db_index=True
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "개인정보 처리방침"
        verbose_name_plural = "개인정보 처리방침 모음"
        db_table = "privacy_policy"
        managed = True


class MarketingConsent(PrintableModel):
    title = models.CharField(null=True, blank=True, max_length=300, help_text="타이틀")

    content = models.TextField(
        max_length=50000,
        blank=True,
        null=True,
        default=None,
        help_text="콘텐츠",
    )

    created_at = models.DateTimeField(db_index=True, default=timezone.now)

    updated_at = models.DateTimeField(
        null=True,
        auto_now=True,
    )
    deleted_at = models.DateTimeField(
        null=True, blank=True, default=None, db_index=True
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "마케팅 수신동의"
        verbose_name_plural = "마케팅 수신동의 모음"
        db_table = "marketing_consent"
        managed = True
