# core/consumers.py
from urllib.parse import parse_qs
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
        query = self.scope['query_string'].decode()
        query= parse_qs(query)
        new_token = query.get('token')[0]
        user_id = query.get('user_id')[0]
        # Register the connection with the token
        websocket_manager.add_connection(new_token, self)
        
        await self.accept()

        if user_id and new_token:
            await self.check_user_logged_in(user_id,new_token)
        await self.send(text_data=json.dumps({ 'message': 'Connected' }))
    
    async def check_user_logged_in(self, user_id,new_token):
         # Fetch existing token for the user
        existing_token = await self.get_existing_token(user_id,new_token)
        
        if existing_token != new_token and existing_token:
            # Notify the previous session to log out
            await websocket_manager.notify_disconnect(existing_token)
            # Replace the old token with the new one
            await self.update_token(user_id, new_token)
            # return
        elif existing_token == new_token:
            # Store the new token
            await self.update_token(user_id, new_token)
        else:
            await self.store_token(user_id,new_token)

        await self.send(text_data=json.dumps({
            'message': 'Login successful',
            'new_token': new_token
        }))

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.send(text_data=json.dumps(data))

    async def disconnect(self, close_code):
        # Remove the connection when the user disconnects
        # print(self.)
        token = self.scope['query_string'].decode().split('=')[1]
        websocket_manager.remove_connection(token,self)


    @staticmethod
    @sync_to_async
    def get_existing_token(user_id, token):
        user = AuthToken.objects.filter(user_id=user_id)
        if user.exists():
            user = user.first()
            return user.token
        return None


    @staticmethod
    @sync_to_async
    def update_token(user_id, new_token):
        # Update the token in the database
        token_record = AuthToken.objects.filter(user_id=user_id).first()
        token_record.token = new_token
        token_record.expires_at = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']+timezone.now()
        token_record.save()

    @staticmethod
    @sync_to_async
    def store_token(user_id, new_token):
        # Store a new token in the database
        AuthToken.objects.create(user_id=user_id, token=new_token,expires_at=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']+timezone.now())
        

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['connection_id']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None,bytes_code=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.scope['user']
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
