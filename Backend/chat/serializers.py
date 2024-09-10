from datetime import timedelta
from django.contrib.humanize.templatetags.humanize import naturalday
from django.utils import timezone 
from rest_framework import serializers

from authentication.models import User
from .models import Connection, Groups , Messages, GroupMembers
from .utils import custom_naturaltime as naturaltime

class ConnectionSerializer(serializers.ModelSerializer):
    friend_info = serializers.SerializerMethodField()
    class Meta:
        model = Connection
        fields = ['id','sender','receiver','connection_id','connected','friend_info']
        extra_kwargs = {
            'id': {'read_only': True},
            'friend_info': {'read_only': True}, 
            # 'sender': {'write_only': True},
            # 'receiver': {'write_only': True},
            
                        }
    def get_friend_info(self, obj)->dict:
        if obj.sender == self.context['user']:
            return obj.receiver.to_dict()
        return obj.sender.to_dict()
    
    
    
    def update(self, instance:Connection, validated_data:dict)->Connection:
        instance.sender = validated_data.get('sender', instance.sender)
        instance.receiver = validated_data.get('receiver', instance.receiver)
        instance.connection_id = validated_data.get('connection_id', instance.connection_id)
        instance.connected = True
        instance.save()
        return instance

class GroupMembersSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    class Meta:
        model = GroupMembers
        fields = ['group','user','role','messages','delete_for_author','delete_for_all','user_info']
        extra_kwargs = {
            'group': {'write_only': True},
            'role': {'write_only': True},
            'messages': {'write_only': True},
            'delete_for_author': {'write_only': True},
            'delete_for_all': {'write_only': True},
        }
    
    def get_user_info(self, obj)->dict:
        return obj.user.to_dict()
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance:GroupMembers, validated_data:dict)->Groups:
        instance.user.add(validated_data.get('user'))
        instance.role = validated_data.get('role', instance.role)
        instance.messages = validated_data.get('messages', instance.messages)
        instance.delete_for_author = validated_data.get('delete_for_author', instance.delete_for_author)
        instance.delete_for_all = validated_data.get('delete_for_all', instance.delete_for_all)
        instance.save()
        return instance

class GroupConnectionSerializer(serializers.ModelSerializer):
    group_members = GroupMembersSerializer(many=True)
    class Meta:
        model = Groups
        fields = ['name','room_id','user']
        extra_kwargs = {'receiver': {'write_only': True}}
    
    
    def create(self, validated_data):
        group_members = validated_data.pop('group_members')
        instance = super().create(validated_data)
        for member in group_members:
            GroupMembers.objects.create(group=instance, **member)
        return instance
        
    def update(self, instance : Groups, validated_data : dict)->Groups:
        group_members = validated_data.pop('group_members')
        for group_member in group_members:
            member = GroupMembers.objects.get(id=group_member['id'])
            self.group_members.update(member, group_member)
        return instance
      
class MessageSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    class Meta:
        model = Messages
        fields = ['id','author','message','connection','delete_for_author','delete_for_all','delete_for_receiver','created_at','updated_at']
        extra_kwargs = {
            'connection': {'write_only': True},
            'id': {'read_only': True},
            'delete_for_author':{'write_only':True},
            'delete_for_all':{'write_only':True},
            'delete_for_receiver':{'write_only':True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            }
   
    def get_created_at(self, obj)->str:
        return f"{naturaltime(obj.created_at)}, {naturalday(obj.created_at,'b d')}".title()
   
    def get_updated_at(self, obj)->str:
        return f"{naturaltime(obj.updated_at)}, {naturalday(obj.updated_at,'b d')}".title()
   
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
    