from urllib.parse import urlencode
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

# Create your views here.

class UserLoginView(TokenObtainPairView):
  serializer_class = CustomTokenObtainPairSerializer
  
  # async def send_notification(self, user_id, new_token):
  #     async with websockets.connect(f'ws://localhost:8000/ws/user-session/?token={new_token}/') as websocket:
  #         await websocket.send(json.dumps({'user_id': user_id, 'token': new_token}))
  #         response = await websocket.recv()
  #         print(response, "line 52 views")
  
  def post(self, request, *args, **kwargs):
    response = super().post(request, *args, **kwargs)
    user = User.objects.get(username=request.data['username'])
    response.data['user_id'] = user.id
    return response
    
  
class UserRefreshView(TokenRefreshView):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]
  def post(self, request: Request, *args, **kwargs) -> Response:
    response = super().post(request, *args, **kwargs)
    expires_at = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] + timezone.now()
    token = AuthToken.objects.get(user = request.user, token = request.auth)
    token.expires_at = expires_at
    token.token = response.data['access']
    token.save()
    return response

class UserSignupView(APIView):
  def post(self, request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

# async def event_stream():
#     i = 0
#     while True:
#         i +=  2
#         # Wait for new notifications
#         time.sleep(2)
#         yield f'data: {i}\n\n'
# def println(request):
#     print("hello")

# def stream_notifications(request):
#     print(request.path)
#     return StreamingHttpResponse(event_stream(), content_type='text/event-stream')