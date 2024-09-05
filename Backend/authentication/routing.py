# routing.py in your app (e.g., yourapp/routing.py)

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/user-session/$', consumers.LoginManagementConsumer.as_asgi()),
]
