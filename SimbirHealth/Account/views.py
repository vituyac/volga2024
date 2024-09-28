from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import NotFound
from django.http import Http404
    
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
    
class GetPostAccounts(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        queryset = User.objects.exclude(is_superuser=True)
        from_p = int(request.GET.get('from', 0))
        count_p = int(request.GET.get('count', queryset.__len__()))
        queryset = User.objects.exclude(is_superuser=True)[from_p-1:from_p + count_p-1]
        serializer = UserNoPSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserRolesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PutDelAccounts(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserRolesSerializer
    queryset = User.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance == request.user:
            return Response({"detail": "Вы не можете удалить себя."}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class GetDoctors(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_doctor=True)
    
class GetDoctorsbyID(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_doctor=True)
    
    def get_object(self):
        try:
            obj = super().get_object()
        except Http404:
            raise NotFound("Доктор с указанным ID не найден.")
        return obj

    
