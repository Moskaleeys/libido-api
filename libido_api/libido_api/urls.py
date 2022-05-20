"""libido_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path

import libido_auths.urls as auth_urls
import libido_services.urls as service_urls
import libido_rooms.urls as rooms_urls
import libido_users.urls as users_urls
import libido_contents.urls as contents_urls
import libido_chats.urls as chats_urls
#import testing.urls as testing_urls

from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="Libido Service API",
        default_version="v1",
        description="v1",
        terms_of_service="Libido",
        contact=openapi.Contact(email="help@libido.co.kr"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path("libido_admin/", admin.site.urls),
    url(r"^v1/", include(auth_urls)),
    url(r"^v1/", include(users_urls)),
    url(r"^v1/", include(service_urls)),
    url(r"^v1/", include(rooms_urls)),
    url(r"^v1/", include(contents_urls)),
    url(r"^v1/", include(chats_urls)),
    path("summernote/", include("django_summernote.urls")),
    url(r"^v9999/auth/", include("rest_framework_social_oauth2.urls")),  # dummpy auth
    #path("test/", include(testing_urls))  # testing purposes
]


urlpatterns += [
    url(
        r"^libido_v1_swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^libido_v1_swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(
        r"^libido_v1_redocs/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
