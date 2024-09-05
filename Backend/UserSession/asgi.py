"""
ASGI config for oauth project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django
from django.conf import settings
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UserSession.settings')
django.setup()

from authentication import routing as auth_routing
from chat import routing as chat_routing
from authentication.middleware import JWTAuthMiddleware


# Make sure the Django setup is complete before any other imports.

from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":JWTAuthMiddleware( 
        URLRouter(
            auth_routing.websocket_urlpatterns +chat_routing.websocket_urlpatterns
            # 
        )
    )
})
