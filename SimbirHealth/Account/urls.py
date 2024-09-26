from django.contrib import admin
from django.urls import path, re_path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    #path('Authentication/SignOut', SignOutView.as_view()),
    
    re_path(r'^Authentication/SignUp/?$', RegistrationAPIView.as_view()),
    re_path(r'^Authentication/Validate/?$', ValidateTokenView.as_view()),
    re_path(r'^Authentication/SignIn/?$', TokenObtainPairView.as_view()),
    re_path(r'^Authentication/Refresh/?$', CustomTokenRefreshView.as_view()),
    re_path(r'^Accounts/Me/?$', MeAPIView.as_view()),
    re_path(r'^Accounts/?$', GetPostAccounts.as_view()),
    re_path(r'^Accounts/(?P<pk>\d+)/?$', PutDelAccounts.as_view()),
    re_path(r'^Doctors/?$', GetDoctors.as_view()),
    re_path(r'^Doctors/(?P<pk>\d+)/?$', GetDoctorsbyID.as_view()),
    
    
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]