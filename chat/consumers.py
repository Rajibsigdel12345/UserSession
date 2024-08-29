import json
import time

from django.db.models import Q
from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import intcomma, naturaltime, naturalday
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Connection , Messages

class ChatUser:
    chat_user = {}
    
class ChatConsumer(AsyncWebsocketConsumer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection_id = None
        self.connection_id = None
    
        
    async def connect(self) -> None:
        self.connection_id = self.scope.get('connection_id',None)
        self.room_name = self.connection_id
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope['user']
        # print(self.scope)
        # print(self.user)
        await self.accept()
        if await self.get_connection(self.user,self.connection_id):
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
        user = self.scope['user']
        time = timezone.now()
        timestamp = f"{naturaltime(time)}  {naturalday(time,format='%b %d')}"
        await self.write_messages(message, user, self.connection_id)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'author': user.to_dict(),
                'created_at': timestamp,
                'updated_at': timestamp
                
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        author = event['author']
        timestamp = {
            'created_at': event['created_at'],
            'updated_at': event['updated_at']
        }
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'author':author,
            **timestamp
        }))
    
    @sync_to_async
    def write_messages(self, message, author, connection):
        Messages.objects.create(message=message, author=author, connection=connection)
    
    @sync_to_async
    def get_connection(self, user,connection_id):
        connection = Connection.objects.filter(
            Q(receiver=user)|Q(sender=user),
            connection_id=connection_id
            )
        if connection.exists():
            self.connection_id = connection.first()
            return connection.first().connected
        return False
