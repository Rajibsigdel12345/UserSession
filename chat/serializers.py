from datetime import timedelta
from django.utils import timezone 
from rest_framework import serializers
from .models import Connection, Groups , Messages

class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ['id','sender','receiver','connection_id','connected']
        extra_kwargs = {'id': {'read_only': True}}
    
    
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
      
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ['id','author','message','connection','delete_for_author','delete_for_all','delete_for_receiver']
        extra_kwargs = {
            'connection': {'write_only': True},
            'id': {'read_only': True},
            'delete_for_author':{'write_only':True},
            'delete_for_all':{'write_only':True},
            'delete_for_receiver':{'write_only':True}
            }
   
    def validate_connection(self, connection):
        if self.instance and connection == self.instance.connection:
            return connection
        raise serializers.ValidationError("You are not authorized to edit this message")
    
    
    # def validate(self, attrs):
    #     if self.instance and self.context['user']!= self.instance.author:
    #         raise serializers.ValidationError("You are not authorized to edit this message")
    #     if self.instance and self.instance.created_at+timedelta(minutes=5) < timezone.now():
    #         raise serializers.ValidationError("Message Edit Time Expired")
    #     return super().validate(attrs)
    
    def update(self, instance:Messages, validated_data:dict)->Messages:
        if instance.author != self.context['user']:
            raise serializers.ValidationError("You are not authorized to edit this message")
        if instance.created_at+timedelta(minutes=5) < timezone.now():
            raise serializers.ValidationError("Message Edit Time Expired")
        instance.author = validated_data.get('author', instance.author)
        instance.message = validated_data.get('message', instance.message)
        instance.connection = validated_data.get('connection', instance.connection)
        instance.save()
        return instance
    
    def delete(self, instance:Messages , validated_data:dict)->None:
        check_time =  instance.created_at+timezone.timedelta(minutes=5) > timezone.now()
        check_user = instance.author == self.context['user']
        
        if validated_data.get('delete_for_self') and check_user:
            instance.delete_for_self = validated_data.get('delete_for_self')
            instance.save()
            return
        
        if not check_user and validated_data.get('delete_for_receiver')is not None:
            instance.delete_for_receiver = validated_data.get('delete_for_receiver')
            instance.save()
            return
        
        if not check_user:
            raise serializers.ValidationError("You are not authorized to delete this message")
        if not check_time and validated_data.get('delete_for_all'):
            raise serializers.ValidationError("You cannot delete this message")
        
        if validated_data.get('delete_for_all'):
            instance.delete_for_all = True
        instance.save()

class MessageReadSerializer(MessageSerializer):
    author = serializers.SerializerMethodField()
    
    def get_author(self, obj)->dict:
        return obj.author.to_dict()
    