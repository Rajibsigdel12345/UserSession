from django.urls import path
from .views import ConnectionView , GroupConnectionView  

urlpatterns = [
  path('add-connection/', ConnectionView.as_view(), name='add-connection'),
  path('add-connection/<int:pk>/', ConnectionView.as_view(), name='add-connection'),
  
]