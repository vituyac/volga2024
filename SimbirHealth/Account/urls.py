from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    #path('Authentication/SignOut', SignOutView.as_view()),
    path('Authentication/SignUp', RegistrationAPIView.as_view()),
    path('Authentication/Validate', ValidateTokenView.as_view()),
    path('Authentication/SignIn', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('Authentication/Refresh', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('Accounts/Me', MeAPIView.as_view()),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]