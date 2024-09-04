# core/consumers.py
from urllib.parse import parse_qs
from django.utils import timezone
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import AuthToken
from .models import AuthToken# Import your JWT token model
from asgiref.sync import sync_to_async
from django.conf import settings
# import time

User = get_user_model()
class WebSocketManager:
    def __init__(self):
        # Dictionary to store the mapping of tokens to WebSocket connections
        self.connections :dict[str:list[LoginManagementConsumer]] = {}

    def add_connection(self, token, connection):
        if not self.connections.get(token):
            self.connections[token] = []
        self.connections[token].append(connection)

    def remove_connection(self, token, connection):
        if token in self.connections:
            self.connections[token].remove(connection)
            # await connection.close()
            print(connection, "closed")

    async def notify_disconnect(self, token:str):
        connections = self.connections.get(token)
        if connections:
            for connection in connections:
                await connection.send(text_data=json.dumps({
                'message': 'logout'
                }))
            # Optionally, close the connection
                await connection.close()
            # Remove the connection from the manager
            del self.connections[token]
    
    def __str__(self):
        return str(self.connections)

websocket_manager = WebSocketManager()

class LoginManagementConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract the token from the query string or headers
        query = self.scope['query_string'].decode()
        query= parse_qs(query)
        new_token = query.get('token')[0]
        user_id = self.scope['user'].id
        print(self.scope['user'], user_id, "inside connect")
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
            print(existing_token)
            await websocket_manager.notify_disconnect(existing_token)
            # Replace the old token with the new one
            await self.update_token(user_id, new_token)
            # return
        elif existing_token == new_token:
            # Store the new token
            # await self.update_token(user_id, new_token)
            pass
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
        query = self.scope['query_string'].decode()
        query= parse_qs(query)
        token = query.get('token')[0]
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
        
