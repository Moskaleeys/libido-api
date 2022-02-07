from django.conf.urls import include, url
from django.urls import path
from django.urls import re_path


from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from libido_auths.views import (
    CustomOauth2TokenView,
    CustomSocialConvertTokenView,
)

urlpatterns = [
    re_path(r"^o/token/$", CustomOauth2TokenView.as_view(), name="token"),
    url(
        r"^o/social-convert-token/?$",
        CustomSocialConvertTokenView.as_view(),
        name="convert_token",
    ),
]
