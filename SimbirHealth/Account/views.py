from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
    
class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    
class ValidateTokenView(APIView):
    
    def get(self, request):
        access_token = request.query_params.get('accessToken')
        if not access_token:
            return Response({"error": "accessToken не предоставлен."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decoded_token = AccessToken(access_token)
            user_id = decoded_token['user_id']
            return Response({"is_valid": "True"})
        except Exception:
            return Response({"is_valid": "False"})

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refreshToken')
        if not refresh_token:
            return Response({"detail": "refreshToken не предоставлен."}, status=status.HTTP_400_BAD_REQUEST)

        data = {'refresh': refresh_token}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class MeAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserNoPSerializer

    def get_object(self):
        return self.request.user
