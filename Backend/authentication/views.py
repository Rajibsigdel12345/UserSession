# from rest_framework.request import Request
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import CustomTokenObtainPairSerializer, SignupSerializer 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import AuthToken , User 
from django.conf import settings
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken 
# Create your views here.
class UserVerifyView(APIView):
  permission_classes = [IsAuthenticated]
  authentication_classes = [JWTAuthentication]
  def post(self, request: 'Request')->Response:
    return Response({'message': 'Token is valid'}, status=status.HTTP_200_OK)
  

  
  # def delete(self, request: 'Request',logout)->Response:
  #   # print(request.auth)
  #   token = AuthToken.objects.filter(user = request.user, token = request.auth)
  #   if not token.exists():
  #     return Response({'message': 'Token is not valid'}, status=status.HTTP_400_BAD_REQUEST)
    
  #   token.delete()
  #   return Response({'message': 'Token is deleted'}, status=status.HTTP_200_OK)

class LogoutView(APIView):
  # authentication_classes = [JWTAuthentication]
  permission_classes= [IsAuthenticated]
  def post(self, request):
        # Get the refresh token from the request
        refresh_token = request.data.get('refresh_token')
        print(request.data)
        
        if not refresh_token:
            print(refresh_token,"line 41")
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            print(token)
            # Blacklist the token
            token.blacklist()
        except Exception as e:
            print(e, "here")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)
  
class UserLoginView(TokenObtainPairView):
  serializer_class = CustomTokenObtainPairSerializer
  def post(self, request:'Request', *args, **kwargs)-> Response:
    response = super().post(request, *args, **kwargs)
    user = User.objects.get(username=request.data['username'])
    response.data['user_id'] = user.id
    return response
    
  
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView

class TokenRefreshView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response({'error': 'Refresh token required'}, status=400)
        
        try:
            # Create a new access token from the refresh token
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            
            # Create the response
            response = Response({
                'access': new_access_token
            })
            
            # Set the new token in the cookie          
            return response
        
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=400)

class UserSignupView(APIView):
  def post(self, request: 'Request')->Response:
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

class UserInfoView(APIView):
  authentication_classes= [JWTAuthentication]
  permission_classes = [IsAuthenticated]
    
  def get (self, reqeust):
    user = reqeust.user
    return Response(user.to_dict(), status=status.HTTP_200_OK)  

