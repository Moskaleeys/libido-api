import bcrypt
from rest_framework import serializers
from libido_services.models import (
    AppVersion,
    TermsOfService,
    PrivacyPolicy,
    MarketingConsent,
)


class AppVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppVersion
        fields = "__all__"


class TermsOfServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsOfService
        fields = "__all__"


class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = "__all__"


class MarketingConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketingConsent
        fields = "__all__"
