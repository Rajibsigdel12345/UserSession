from django.urls import path
from .views import ConnectionView , GroupConnectionView ,MessageView, UserListView

urlpatterns = [
  path('add-connection/', ConnectionView.as_view(), name='add-connection'),
  # path('add-connection/<slug:pending>', ConnectionView.as_view(), name='add-connection'),
  path('add-connection/<int:pk>/', ConnectionView.as_view(), name='add-connection'),
  path('message/', MessageView.as_view(), name='message'),
  path('message/<int:pk>/', MessageView.as_view(), name='message'),
  path('user-list/', UserListView.as_view(), name='user-list'),
  
]