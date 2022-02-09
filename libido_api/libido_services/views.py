from django.shortcuts import render
from rest_framework import status, viewsets, mixins
from libido_commons import permissions
from libido_services.models import (
    AppVersion,
    PrivacyPolicy,
    TermsOfService,
    MarketingConsent,
)
from libido_commons.paginations import CommonPagination
from libido_services.serializers import (
    AppVersionSerializer,
    PrivacyPolicySerializer,
    TermsOfServiceSerializer,
    MarketingConsentSerializer,
)
from libido_commons import renderers
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response


class ServiceBaseViewSet(
    mixins.ListModelMixin,  # retrive open -> user_id retrive
    mixins.RetrieveModelMixin,  # retrive open -> user_id retrive
    viewsets.GenericViewSet,
):
    pass


class AppVersionViewSet(ServiceBaseViewSet):
    __basic_fields = ("id", "os", "current_version", "min_version")
    permission_classes = [
        permissions.AllowRetriveList,
    ]
    renderer_classes = [renderers.LibidoApiJSONRenderer]
    queryset = (
        AppVersion.objects.all().exclude(deleted_at__isnull=False).order_by("-id")
    )
    serializer_class = AppVersionSerializer
    pagination_class = CommonPagination
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filter_fields = __basic_fields
    search_fields = __basic_fields


class PrivacyPolicyViewSet(ServiceBaseViewSet):
    __basic_fields = ("id", "title", "content")
    permission_classes = [
        permissions.AllowRetriveList,
    ]
    queryset = (
        PrivacyPolicy.objects.all().exclude(deleted_at__isnull=False).order_by("-id")
    )
    serializer_class = PrivacyPolicySerializer
    pagination_class = CommonPagination
    renderer_classes = [renderers.LibidoApiJSONRenderer]
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filter_fields = __basic_fields
    search_fields = __basic_fields


class TermsOfServiceViewSet(ServiceBaseViewSet):
    __basic_fields = ("id", "title", "content")
    permission_classes = [
        permissions.AllowRetriveList,
    ]
    queryset = (
        TermsOfService.objects.all().exclude(deleted_at__isnull=False).order_by("-id")
    )
    serializer_class = TermsOfServiceSerializer
    pagination_class = CommonPagination
    renderer_classes = [renderers.LibidoApiJSONRenderer]
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filter_fields = __basic_fields
    search_fields = __basic_fields


class MarketingConsentViewSet(ServiceBaseViewSet):
    __basic_fields = ("id", "title", "content")
    permission_classes = [
        permissions.AllowRetriveList,
    ]
    queryset = (
        MarketingConsent.objects.all().exclude(deleted_at__isnull=False).order_by("-id")
    )
    serializer_class = MarketingConsentSerializer
    pagination_class = CommonPagination
    renderer_classes = [renderers.LibidoApiJSONRenderer]
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filter_fields = __basic_fields
    search_fields = __basic_fields
