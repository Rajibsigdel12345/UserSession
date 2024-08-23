from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        return token
      
class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email', 'password','first_name','last_name']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        data = {
          'username':validated_data['username'],
          'email':validated_data['email'],
          'password':validated_data['password'],
          'first_name':validated_data['first_name'], 
          'last_name':validated_data['last_name']
        }
        user = User.objects.create_user(**data)
        return user