from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
    
class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer