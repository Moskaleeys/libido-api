from .base import *
from boto3.session import Session
import os


DEBUG = False

SERVICE = "product"
ALLOWED_HOSTS = ["*"]

# WSGI_APPLICATION = "libido_api.wsgi.development.application"

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_ACCESS_KEY_ID = "AKIATWD4P5YETFG735QQ"
AWS_SECRET_ACCESS_KEY = "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"

AWS_STORAGE_BUCKET_NAME = "libido-dev"

# AWS_DEFAULT_ACL = "public-read"

AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}

AES_SECRET_KEY = "TOTEMc3RhedW5nZXJ5LXN0YXkhLWZvb2xpc2hAc3RldmE"

AWS_LOCATION = "static"
AWS_S3_ENCRYPTION = True
AWS_S3_CUSTOM_DOMAIN = "%s.s3.ap-northeast-2.amazonaws.com" % AWS_STORAGE_BUCKET_NAME
# AWS_S3_CUSTOM_DOMAIN = CLOUDFRONT_DOMAIN

STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

MEDIA_URL = "http://%s/static/" % AWS_S3_CUSTOM_DOMAIN
MEDIA_ROOT = os.path.join(AWS_S3_CUSTOM_DOMAIN, "offerflow")

LANGUAGE_CODE = "en-US"
TIME_ZONE = "Asia/Seoul"
AWS_REGION_NAME = "ap-northeast-2"

boto3_session = Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME,
)

if "DATABASE_HOST" in os.environ:
    # Running the Docker image with configs
    DATABASES["default"]["ENGINE"] = os.getenv("DATABASE_ENGINE")
    DATABASES["default"]["HOST"] = os.getenv("DATABASE_HOST")
    DATABASES["default"]["PORT"] = os.getenv("DATABASE_PORT")
    DATABASES["default"]["NAME"] = os.getenv("DATABASE_NAME")
    DATABASES["default"]["USER"] = os.getenv("DATABASE_USER")
    DATABASES["default"]["PASSWORD"] = os.getenv("DATABASE_PASSWORD")
    DATABASES["default"]["OPTIONS"] = {
        "charset": "utf8mb4",  # prevent 1366, "Incorrect string value: '\\xEC\\x82\\xAC\\xEC\\x9A\\xA9...' for colum
        "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
    }


if "CACHES_BACKEND" in os.environ:
    CACHES["default"]["BACKEND"] = os.getenv("CACHES_BACKEND")
    CACHES["default"]["KEY_PREFIX"] = os.getenv("CACHES_KEY_PREFIX")
    CACHES["default"]["LOCATION"] = os.getenv("CACHES_LOCATION")
    CACHES["default"]["OPTIONS"] = {
        "CLIENT_CLASS": "django_redis.client.DefaultClient",
    }

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django.request.aws": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "sentry.errors": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "default": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

FCM_SERVER_KEY = "AAAs1wDg:APAeoP0jzvrO4cQp29B4tKP1kSnSaf4zJzoYG4D9znQsj9ihB5LI9HcQHWBUAHek5SN4hDL5WSP4Q0DCXktk27GiNBo2Cy31NgJdjl9enLl9r22TYA7CmoXjI"

# KEYFILES_DIR = os.path.join(BASE_DIR, "credentials")
# FIREBASE_KEY = "jupiter-2b5d0-firebase-adminsdk-skp17-923cbae407.json"

FCM_DJANGO_SETTINGS = {
    # default: _('FCM Django')
    "APP_VERBOSE_NAME": "LIBIDO-API",
    # Your firebase API KEY
    "FCM_SERVER_KEY": FCM_SERVER_KEY,
    # true if you want to have only one active device per registered user at a time
    # default: False
    "ONE_DEVICE_PER_USER": True,
    # devices to which notifications cannot be sent,
    # are deleted upon receiving error response from FCM
    # default: False
    "DELETE_INACTIVE_DEVICES": True,
}

# PUSH_SERVICE = FCMNotification(api_key=FCM_SERVER_KEY)

# CACHES_LOCATION: "redis://redis:6379/1"
# 개발서버만 해당 docker-compose 의 redis를 사용함..
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}

# social naver
SOCIAL_AUTH_NAVER_KEY = "ipyqHeQ5gpL7mwpyGadxL"
SOCIAL_AUTH_NAVER_SECRET = "NCBZKqpex8C"


# social google
SOCIAL_AUTH_GOOGLE_OAUTH_KEY = "AIzaSyDiAIch5CT4xH02m2dWAXLOQi8BDyyrzrY"
SOCIAL_AUTH_GOOGLE_OAUTH_SECRET = ""
