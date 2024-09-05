from django.urls import path
from .views import ConnectionView , GroupConnectionView ,MessageView

urlpatterns = [
  path('add-connection/', ConnectionView.as_view(), name='add-connection'),
  path('add-connection/<int:pk>/', ConnectionView.as_view(), name='add-connection'),
  path('message/', MessageView.as_view(), name='message'),
  path('message/<int:pk>/', MessageView.as_view(), name='message'),
  
]