from django.http.response import Http404
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Prefetch


from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.settings import api_settings


class DeleteMixin(object):
    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()
