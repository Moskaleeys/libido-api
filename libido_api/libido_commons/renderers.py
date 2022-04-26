import time
import logging
from rest_framework.renderers import JSONRenderer

from django.shortcuts import resolve_url
from django.template.loader import render_to_string
from django.utils.encoding import force_str
from django.utils.functional import Promise
from rest_framework.renderers import BaseRenderer, JSONRenderer, TemplateHTMLRenderer
from rest_framework.utils import encoders, json

from drf_yasg.app_settings import redoc_settings, swagger_settings
from drf_yasg.codecs import VALIDATORS, OpenAPICodecJson, OpenAPICodecYaml
from drf_yasg.openapi import Swagger
from drf_yasg.utils import filter_none

request_logger = logging.getLogger("default")


class LibidoApiJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        request_logger.info(data)
        if status_code == 204:  # if delete method success...
            response = {
                "message_code": 200,
                "message": "Content Delete Success",
                "data": None,
            }
            return super(LibidoApiJSONRenderer, self).render(
                response, accepted_media_type, renderer_context
            )

        if "detail" in data:
            # 에러 exception 인경우임
            if status_code == 404:
                response = {
                    "message_code": 404,
                    "message": "Not found",
                    "data": None,
                }
            else:
                try:
                    message = str(data["detail"])
                    message_code = int(data["detail"].code)
                    response = {
                        # 'timnestamp': int(time.time()),
                        # 'success': True,
                        # 'status_code': status_code,
                        "message_code": message_code,
                        "message": message,
                        "data": None,
                        # 'status_code': 200, # 200 고정임
                        # 'result': {
                        #     'msg': '',
                        #     'msg_code': '200',
                        #     'data': data,
                        # },
                        # 'error': message,
                        # 'error_code': message_code,
                    }

                except Exception as e:
                    # def default error 케이스인경우
                    message = str(data["detail"])
                    response = {
                        # 'timnestamp': int(time.time()),
                        # 'success': True,
                        # 'status_code': status_code,
                        "message_code": status_code,
                        "message": message,
                        "data": None,
                        # 'status_code': 200, # 200 고정임
                        # 'result': {
                        #     'msg': '',
                        #     'msg_code': '200',
                        #     'data': data,
                        # },
                        # 'error': message,
                        # 'error_code': message_code,
                    }

        elif ("detail" not in data) and (status_code in [200, 201, 202]):
            response = {
                # 'timnestamp': int(time.time()),
                # 'success': True,
                # 'status_code': status_code,
                "message_code": 100,
                "message": "success",
                "data": data,
                # 'status_code': 200, # 200 고정임
                # 'result': {
                #     'msg': '',
                #     'msg_code': '200',
                #     'data': data,
                # },
                # 'error': '',
                # 'error_code': '',
            }
        else:
            # 기본 400 에러인경우
            response = {
                # 'timnestamp': int(time.time()),
                # 'success': True,
                # 'status_code': status_code,
                "message_code": status_code,
                "message": data,
                "data": None,
                # 'status_code': 200, # 200 고정임
                # 'result': {
                #     'msg': '',
                #     'msg_code': '200',
                #     'data': data,
                # },
                # 'error': '',
                # 'error_code': '',
            }

        return super(LibidoApiJSONRenderer, self).render(
            response, accepted_media_type, renderer_context
        )


class _SpecRenderer(BaseRenderer):
    """Base class for text renderers. Handles encoding and validation."""

    charset = "utf-8"
    validators = []
    codec_class = None

    @classmethod
    def with_validators(cls, validators):
        assert all(
            vld in VALIDATORS for vld in validators
        ), "allowed validators are " + ", ".join(VALIDATORS)
        return type(cls.__name__, (cls,), {"validators": validators})

    def render(self, data, media_type=None, renderer_context=None):
        assert self.codec_class, "must override codec_class"
        codec = self.codec_class(self.validators)

        if not isinstance(data, Swagger):  # pragma: no cover
            # if `swagger` is not a ``Swagger`` object, it means we somehow got a non-success ``Response``
            # in that case, it's probably better to let the default ``JSONRenderer`` render it
            return LibidoApiJSONRenderer().render(data, media_type, renderer_context)
            # see https://github.com/axnsan12/drf-yasg/issues/58

        return codec.encode(data)


class SwaggerJSONRenderer(_SpecRenderer):
    """Renders the schema as a JSON document with the generic ``application/json`` mime type."""

    media_type = "application/json"
    format = ".json"
    codec_class = OpenAPICodecJson


class OpenAPIRenderer(_SpecRenderer):
    """Renders the schema as a JSON document with the ``application/openapi+json`` specific mime type."""

    media_type = "application/openapi+json"
    format = "openapi"
    codec_class = OpenAPICodecJson
