
import datetime
from django.utils import timezone
from django.conf import settings
from rest_framework.response import Response
from django.http import JsonResponse
import json
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from rest_framework_simplejwt.backends import TokenBackend
from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework.renderers import JSONRenderer
import time
from .models import AuthToken  # Assuming you have an AuthToken model

User = get_user_model()

@database_sync_to_async
def get_user(email):
    try:
        user = get_user_model()
        return user.objects.get(email=email)
    except user.DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Extract the token from the query string
        query_string = parse_qs(scope["query_string"].decode())
        # print(query_string)
        token = query_string.get('token', [None])[0]
        connection_id= query_string.get('connection_id', [None])[0] 
        
        # print(token)
        if token:
            # print("here"
            try:
                # Decode the JWT token
                access_token = TokenBackend(algorithm="HS256").decode(token, verify=False)
                if access_token.get('token_type') != 'access':
                    raise PermissionError('Invalid token type')
                if not access_token.get('exp'):
                    await self.send_logout_message(send)
                if access_token.get('exp') < int(time.time()):
                    await self.send_logout_message(send)
                user_id = access_token['email']
                scope['user'] = await get_user(user_id)
            except Exception:
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()

        # Proceed with the connection if user is authenticated
        if scope['user'].is_authenticated:
            return await super().__call__(scope, receive, send)
        else:
            # If the user is not authenticated, close the connection
            await send({
                'type': 'websocket.close',
                'code': 4001
            })
        if connection_id:
            self.scope['url_route']['kwargs']['connection_id']= connection_id

    async def send_logout_message(self, send):
        await send({
            'type': 'websocket.send',
            'text': json.dumps({"action": "logout"})
        })
        await send({
            'type': 'websocket.close',
            'code': 4001  # Custom close code for forced logout
        })

            
            




class MaxLoginMiddleware(BaseMiddleware):
    def get_active_user_count(self):
    # Assuming your AuthToken model has a `user` ForeignKey and an `expires_at` datetime field
        active_tokens = AuthToken.objects.filter(expires_at__gt=timezone.now()).count()
        return active_tokens

    def __init__(self, get_response):
        self.get_response = get_response
        self.max_active_users = settings.MAX_ACTIVE_USERS  # Set your maximum allowed users here

    def __call__(self, request):
        # Check if the request is for login
        if request.path == '/token/' and request.method == 'POST' or request.path == '/token/refresh/':  # Assuming '/api/token/' is your login URL
            active_user_count = self.get_active_user_count()
            print(time.time(), active_user_count)
            if active_user_count >= self.max_active_users:
                response_data = {'error': 'Maximum number of active users reached'}
                return JsonResponse(response_data, safe=False, status=403)
        
        response = self.get_response(request)
        return response

class TokenCleanUPMiddleware(BaseMiddleware):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (request.path == '/token/' or request.path == '/token/refresh/') and request.method == 'POST':
        # Clean up expired tokens
            AuthToken.objects.filter(expires_at__lt=timezone.now()).delete()
        response = self.get_response(request)
        return response
