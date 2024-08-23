# core/consumers.py
from django.utils import timezone
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import AuthToken
from UserSession.websocket_manager import websocket_manager  # Import the WebSocket manager
from .models import AuthToken# Import your JWT token model
from asgiref.sync import sync_to_async
from django.conf import settings
# import time

User = get_user_model()

class LoginManagementConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract the token from the query string or headers
        token = self.scope['query_string'].decode().split('=')[1]
        
        # Register the connection with the token
        websocket_manager.add_connection(token, self)
        
        await self.accept()
        await self.send(text_data=json.dumps({ 'message': 'Connected' }))

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_id = data.get('user_id')
        new_token = data.get('token')
        # print(user_id, new_token, "line 26 consumers")

        if user_id and new_token:
            # Fetch existing token for the user
            existing_token = await self.get_existing_token(user_id,new_token)
            
            if existing_token:
                # Notify the previous session to log out
                await websocket_manager.notify_disconnect(existing_token)
                # Replace the old token with the new one
                await self.update_token(user_id, new_token)
                # return
            else:
                # Store the new token
                await self.store_token(user_id, new_token)

            await self.send(text_data=json.dumps({
                'message': 'Login successful',
                'new_token': new_token
            }))

    async def disconnect(self, close_code):
        # Remove the connection when the user disconnects
        token = self.scope['query_string'].decode().split('=')[1]
        websocket_manager.remove_connection(token)


    @staticmethod
    @sync_to_async
    def get_existing_token(user_id, token):
        user = AuthToken.objects.filter(user_id=user_id)
        if user.exists():
            user = user.first()
            # print(user.token, token, "line 56 consumers")
            # if user.token != token:
            return user.token
        return None


    @staticmethod
    @sync_to_async
    def update_token(user_id, new_token):
        # Update the token in the database
        token_record = AuthToken.objects.filter(user_id=user_id).first()
        token_record.token = new_token
        # print(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])
        token_record.expires_at = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']+timezone.now()
        token_record.save()

    @staticmethod
    @sync_to_async
    def store_token(user_id, new_token):
        # Store a new token in the database
        user = AuthToken.objects.create(user_id=user_id, token=new_token,expires_at=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']+timezone.now())
