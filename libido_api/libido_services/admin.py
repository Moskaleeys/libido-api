from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from libido_services.models import (
    TermsOfService,
    PrivacyPolicy,
    AppVersion,
    MarketingConsent,
)

# Register your models here.


class AppVersionAdmin(admin.ModelAdmin):
    list_display = ["os", "current_version", "min_version", "created_at"]
    list_display_links = ["os", "current_version", "min_version", "created_at"]


class TermsOfServiceAdmin(SummernoteModelAdmin):
    search_fields = ["id", "title"]
    list_display = [
        "id",
        "title",
        "created_at",
        "deleted_at",
    ]

    list_display_links = [
        "id",
        "title",
        "created_at",
        "deleted_at",
    ]


class MarketingConsentAdmin(SummernoteModelAdmin):
    search_fields = ["id", "title"]
    list_display = [
        "id",
        "title",
        "created_at",
        "deleted_at",
    ]

    list_display_links = [
        "id",
        "title",
        "created_at",
        "deleted_at",
    ]


class PrivacyPolicyAdmin(SummernoteModelAdmin):
    search_fields = ["id", "title"]
    list_display = [
        "id",
        "title",
        "created_at",
        "deleted_at",
    ]

    list_display_links = [
        "id",
        "title",
        "created_at",
        "deleted_at",
    ]


admin.site.register(TermsOfService, TermsOfServiceAdmin)
admin.site.register(PrivacyPolicy, PrivacyPolicyAdmin)
admin.site.register(MarketingConsent, MarketingConsentAdmin)
admin.site.register(AppVersion, AppVersionAdmin)
