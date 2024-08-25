import json
import re

from django.db.models import Q
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Connection


class ChatConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def get_connection(self, user,connection_id):
        connection = Connection.objects.filter(
            Q(receiver=user)|Q(sender=user),
            connection_id=connection_id
            )
        if connection.exists():
            return connection.first().connected
        return False
    
        
    async def connect(self) -> None:
        connection_id = self.scope.get('connection_id',None)
        self.room_name = connection_id
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope['user']
        # print(self.scope)
        print(self.user)
        await self.accept()
        print(await self.get_connection(self.user,connection_id), "awaiting")
        if await self.get_connection(self.user,connection_id):
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
        # Join room group
        else:
            # await self.accept()
            await self.send(text_data=json.dumps({
                'message': 'You are not authorized to enter this room'
            }))
            await self.close(code=4001 , reason='Unauthorized')

    async def disconnect(self, close_code) -> None:
        # Leave room group
        pass

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
            'message': message,
            'user':self.scope['user'].username
        }))
