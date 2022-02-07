import json
import logging
import urllib.parse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, View
from oauth2_provider.models import get_access_token_model, get_application_model
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.signals import app_authorized
from oauth2_provider.views.base import TokenView
from oauth2_provider.views.mixins import OAuthLibMixin
from rest_framework import status, viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view, renderer_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_social_oauth2.oauth2_backends import KeepRequestCore
from rest_framework_social_oauth2.oauth2_endpoints import SocialTokenServer

from libido_commons import exceptions
from libido_commons.renderers import LibidoApiJSONRenderer
from libido_users.models import User


class CsrfExemptMixin(object):
    """
    Exempts the view from CSRF requirements.
    NOTE:
        This should be the left-most mixin of a view.
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CsrfExemptMixin, self).dispatch(*args, **kwargs)


class CustomOauth2TokenView(TokenView):
    @method_decorator(sensitive_post_parameters("password"))
    @renderer_classes([LibidoApiJSONRenderer])
    def post(self, request, *args, **kwargs):
        from django.http import JsonResponse

        url, headers, body, status = self.create_token_response(request)
        print(request.__dict__)
        print("*" * 10)
        data = json.loads(body)
        print(data)
        if status == 200:
            access_token = json.loads(body).get("access_token")
            if access_token is not None:
                token = get_access_token_model().objects.get(token=access_token)
                app_authorized.send(sender=self, request=request, token=token)

                response = {
                    "message_code": 100,
                    "message": "success",
                    "data": data,
                }
                return JsonResponse(response, status=status)

        if status in [400, 401, 403]:
            if data["error"] == "invalid_grant":
                username = request._post["username"]

                if not User.is_exists(username=username):
                    response = {
                        "message_code": 1110,
                        "message": "UserIdNotFoundError",
                        "data": None,
                    }
                    return JsonResponse(response, status=200)

                    # raise exceptions.UserIdNotFoundError

                if data["error_description"] == "Invalid credentials given.":
                    # raise exceptions.InvalidUserPasswordError
                    response = {
                        "message_code": 1111,
                        "message": "InvalidUserPasswordError",
                        "data": None,
                    }
                    return JsonResponse(response, status=200)

            elif data["error"] == "invalid_client":
                response = {
                    "message_code": 1112,
                    "message": "InvalidOauth2ClientIdOrSecretError",
                    "data": None,
                }
                # return JsonResponse(response, status=status)
                return JsonResponse(response, status=200)

            elif data["error"] == "unsupported_grant_type":
                response = {
                    "message_code": 1113,
                    "message": "UnSupportedGrantTypeError",
                    "data": None,
                }
                return JsonResponse(response, status=200)

        # finally
        response = {
            "message_code": 99999,
            "message": "Unknown Error",
            "data": data,
        }
        return JsonResponse(response, status=200)


class CustomSocialConvertTokenView(CsrfExemptMixin, OAuthLibMixin, APIView):
    """
    Implements an endpoint to convert a provider token to an access token
    The endpoint is used in the following flows:
    * Authorization code
    * Client credentials
    """

    server_class = SocialTokenServer
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = KeepRequestCore
    permission_classes = (permissions.AllowAny,)
    renderer_classes = [LibidoApiJSONRenderer]

    def post(self, request, *args, **kwargs):
        # Use the rest framework `.data` to fake the post body of the django request.
        mutable_data = request.data.copy()
        request._request.POST = request._request.POST.copy()
        for key, value in mutable_data.items():
            request._request.POST[key] = value

        url, headers, body, status = self.create_token_response(request._request)
        response = Response(data=json.loads(body), status=status)

        for k, v in headers.items():
            response[k] = v
        return response
