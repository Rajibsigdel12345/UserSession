from rest_framework import serializers
from .models import Connection, Groups

class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ['sender','receiver','connection_id']
        extra_kwargs = {'sender': {'write_only': True}, 'receiver': {'write_only': True}}
    
    
    def update(self, instance:Connection, validated_data:dict)->Connection:
        instance.sender = validated_data.get('sender', instance.sender)
        instance.receiver = validated_data.get('receiver', instance.receiver)
        instance.connection_id = validated_data.get('connection_id', instance.connection_id)
        instance.connected = True
        instance.save()
        return instance

class GroupConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = ['name','room_id','user']
        extra_kwargs = {'receiver': {'write_only': True}}
    
    def update(self, instance : Groups, validated_data : dict)->Groups:
        instance.admin.add(validated_data.get('admin'))
        instance.name = validated_data.get('name', instance.name)
        instance.room_id = validated_data.get('room_id', instance.room_id)
        instance.user.add(validated_data.get('user')) 
        instance.save()
        return instance