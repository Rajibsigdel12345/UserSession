from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from rest_framework.request import Request
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ConnectionSerializer, GroupConnectionSerializer , MessageSerializer , MessageReadSerializer
from .models import Groups , Connection, Messages
from authentication.models import User
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
class ConnectionView(APIView):
  serializer_class = ConnectionSerializer
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]
  
  def get_object(self,request :'Request',pk: int| None =None)->Connection| list[Connection]:
    if request.method == 'GET':
      return Connection.objects.filter(Q(sender = request.user) | Q(receiver = request.user))
    if request.method == "PUT" and pk:
      return Connection.objects.get(receiver = request.user, id = pk)
    if request.method == "DELETE" and pk:
      return Connection.objects.get(Q(sender = request.user) | Q(receiver = request.user), id = pk)
    raise Http404("Invalid Request")
    
  def get(self, request :'Request')->Response:
    queryset = self.get_object(request)
    serializer = self.serializer_class(queryset, many=True,context={'user':request.user})
    return Response(serializer.data)
  
  def post(self, request:'Request')->Response:
    data  =request.data
    data['sender'] = request.user.id
    serializer = self.serializer_class(data = data, context={'user':request.user})
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def put(self, request:'Request', pk:int)->Response:
    instance = self.get_object(request, pk)
    if instance.connected:
      return Response({"message":"Connection already established"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = self.serializer_class(instance = instance, data=request.data, partial = True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def delete(self, request:'Request', pk:int)->Response:
    instance = self.get_object(request=request, pk=pk)
    instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  


class GroupConnectionView(APIView):
  serializer_class = GroupConnectionSerializer
  
  def get_object(self, pk :int)->Groups:
    return get_object_or_404(Groups, pk=pk)
  
  def post(self, request:'Request')->Response:
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def put(self,request :'Request' , pk:int)->Response:
    instance = self.get_object(pk)
    serializer = self.serializer_class(instance = instance,data=request.data, partial= True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class MessageView(APIView):
    serializer_class = {
      'read':MessageReadSerializer,
      'write':MessageSerializer
      }
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_serializer(self, *args, **kwargs)->MessageSerializer|MessageReadSerializer:
      if self.request.method == 'GET':
        return self.serializer_class['read'](*args,**kwargs)
      return self.serializer_class['write'](*args,**kwargs)
    
    def get_object(self,request:'Request', pk:int)->Messages:
      return get_object_or_404(Messages, pk=pk)
    
    def get(self, request:'Request')->Response:
      params = request.query_params.get('connection_id',None)
      if_connected = Q(connection__receiver = request.user)|Q(connection__sender = request.user)
      queryset = Messages.objects.filter(
        if_connected
      ,connection__connection_id = params
        ).exclude(
          (Q(delete_for_author = True)&Q(author= request.user))|
          (Q(delete_for_receiver = True)& ~Q( author= request.user))
            ).exclude(
              Q(delete_for_all = True)
            )
      serializer = self.get_serializer(queryset, many=True)
      return Response(serializer.data)
        
    def put(self, request:'Request', pk:int)->Response:
      instance = self.get_object(request, pk)
      serializer = self.get_serializer(instance = instance, data=request.data, partial = True, context={'user':request.user})
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request:'Request', pk:int)->Response:
      instance = self.get_object(request, pk)
      data = request.data
      serializer = self.get_serializer(instance = instance, data = data,partial=True, context = {'user':request.user})
      if serializer.is_valid(raise_exception=True):
        validated_data = serializer.validated_data
        serializer.delete(instance,validated_data)
        # serializer.save()
      return Response(status=status.HTTP_204_NO_CONTENT)
    
class UserListView(APIView):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]
  def get(self, reqeust: 'Request')->Response:
    users = User.objects.all().exclude(id = reqeust.user.id)
    connection = Connection.objects.filter(Q(sender = reqeust.user)|Q(receiver = reqeust.user))
    users = [user.to_dict() for user in users if not connection.filter(Q(sender = user)|Q(receiver = user)).exists()]
    return Response(users, status=status.HTTP_200_OK)