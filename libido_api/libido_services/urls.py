from django.conf.urls import include, url
from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from libido_services.views import (
    TermsOfServiceViewSet,
    PrivacyPolicyViewSet,
    AppVersionViewSet,
    MarketingConsentViewSet,
)


default_router = DefaultRouter(trailing_slash=False)

default_router.register(r"app_versions", AppVersionViewSet, basename="app_versions")
default_router.register(
    r"terms_of_services", TermsOfServiceViewSet, basename="terms_of_service"
)

default_router.register(
    r"privacy_policy", PrivacyPolicyViewSet, basename="privacy_policy"
)

default_router.register(
    r"marketing_consent", MarketingConsentViewSet, basename="marketing_consent"
)


urlpatterns = [
    url(r"^", include(default_router.urls)),
]
