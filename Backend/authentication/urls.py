from django.urls import path
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserLoginView, UserRefreshView, UserSignupView, UserVerifyView
urlpatterns = [
  # path('login/', UserLoginView.as_view(), name='login'),
  path('', UserLoginView.as_view(), name='login'),
  path('refresh/', UserRefreshView.as_view(), name='refresh'),
  path('signup/', UserSignupView.as_view(), name='signup'),
  path('verify/', UserVerifyView.as_view(), name='verify'),
  path('<slug:logout>/', UserVerifyView.as_view(), name='logout'),
  # path('stream/', stream_notifications, name='stream'),
  # path('stream/', println, name='stream'),
]