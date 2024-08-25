from rest_framework import serializers
from .models import Connection, Groups

class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ['sender','receiver','connection_id']
        extra_kwargs = {'sender': {'write_only': True}, 'receiver': {'write_only': True}}

class GroupConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = ['name','room_id','user']
        extra_kwargs = {'receiver': {'write_only': True}}
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.room_id = validated_data.get('room_id', instance.room_id)
        instance.user.add(validated_data.get('user', instance.user)) 
        instance.save()
        return instance