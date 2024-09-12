from django.urls import path
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserLoginView, UserSignupView, UserVerifyView, UserInfoView, LogoutView,TokenRefreshView
urlpatterns = [
  # path('login/', UserLoginView.as_view(), name='login'),
  path('token/', UserLoginView.as_view(), name='login'),
  # path('token/refresh/', UserRefreshView.as_view(), name='refresh'),
  path('token/signup/', UserSignupView.as_view(), name='signup'),
  path('token/verify/', UserVerifyView.as_view(), name='verify'),
  path('token/logout/', LogoutView.as_view(), name='logout'),
  path('me/', UserInfoView.as_view(), name='me'),
  path('token/refresh/', TokenRefreshView.as_view(), name='refresh'),
  # path('stream/', stream_notifications, name='stream'),
  # path('stream/', println, name='stream'),
]