"""
ASGI config for libido_api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "libido_api.settings")

application = get_asgi_application()


from libido_commons.middlewares import TokenAuthMiddleware
from libido_chats.routing import websocket_urlpatterns
from libido_chats.token_auth import TokenAuthMiddlewareStack

application = ProtocolTypeRouter(
    {
        "http": application,
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)

# application = ProtocolTypeRouter(
#     {
#         "http": application,
#         "websocket": AllowedHostsOriginValidator(
#             TokenAuthMiddleware(URLRouter(websocket_urlpatterns))
#         ),
#     }
# )
