from django.contrib import admin
from django.urls import path, re_path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    
    re_path(r'^api/Authentication/SignOut/?$', SignOutView.as_view()),
    re_path(r'^api/Authentication/SignUp/?$', RegistrationAPIView.as_view()),
    re_path(r'^api/Authentication/Validate/?$', ValidateTokenView.as_view()),
    re_path(r'^api/Authentication/SignIn/?$', TokenObtainPairView.as_view()),
    re_path(r'^api/Authentication/Refresh/?$', CustomTokenRefreshView.as_view()),
    re_path(r'^api/Accounts/Me/?$', MeAPIView.as_view()),
    re_path(r'^api/Accounts/?$', GetPostAccounts.as_view()),
    re_path(r'^api/Accounts/Update/?$', AccountsUpdateAPIView.as_view()),
    re_path(r'^api/Accounts/(?P<pk>\d+)/?$', PutDelAccounts.as_view()),
    re_path(r'^api/Doctors/?$', GetDoctors.as_view()),
    re_path(r'^api/Doctors/(?P<pk>\d+)/?$', GetDoctorsbyID.as_view()),
    
    
    #path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]