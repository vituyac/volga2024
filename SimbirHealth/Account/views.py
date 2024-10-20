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
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg import openapi
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

class SignOutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Добавление refresh токена в чёрный спискок",
        operation_description="Только авторизованные пользователи"
    )
    def put(self, request, *args, **kwargs):
        user = request.user.id
        try:
            outstanding_token = OutstandingToken.objects.filter(user_id=user).order_by('-created_at').first()
            print(outstanding_token)
        except OutstandingToken.DoesNotExist:
            return Response({"detail": "Токен не найден."}, status=status.HTTP_404_NOT_FOUND)
        BlacklistedToken.objects.create(token=outstanding_token)
        return Response({"detail": "Refresh токен больше не действителен."}, status=status.HTTP_200_OK)
        

class AccountsUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserUpSerializer
    permission_classes = [IsAuthenticated]

    http_method_names = ['put']
    
    @swagger_auto_schema(
        operation_summary="Обновление своего аккаунта",
        operation_description="Только авторизованные пользователи"
    )
    def put(self, request, *args, **kwargs):
        user = request.user
        print(user)
        new_password = request.data.get('password', None)
        lname = request.data.get('lastName', None)
        fname = request.data.get('firstName', None)
        if lname:
            user.last_name = lname
        if fname:
            user.first_name = fname
        serializer = self.get_serializer(user, data=request.data)

        serializer.is_valid(raise_exception=True)

        if new_password:
            user.password = make_password(new_password)

        user.save()
        return Response(serializer.data)

    def get_object(self):
        return self.request.user
    
    
class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    
    @swagger_auto_schema(
        operation_summary="Регистрация пользователя",
        operation_description="Позволяет зарегистрировать нового пользователя."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
class ValidateTokenView(APIView):
    
    @swagger_auto_schema(
        operation_summary="Интроспекция токена",
        operation_description="Интроспекция токена",
        manual_parameters = [
            openapi.Parameter(
                'accessToken',
                openapi.IN_QUERY,
                description="Передаётся в query параметрах",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
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

    @swagger_auto_schema(
        operation_summary="Обновление access токена по refresh токену",
        operation_description="Обновление access токена по refresh токену",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refreshToken': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    title="refreshToken",
                    description="refreshToken"
                ),
            },
            required=['refreshToken']
        ),
    )
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refreshToken')
        if not refresh_token:
            return Response({"detail": "refreshToken не предоставлен."}, status=status.HTTP_400_BAD_REQUEST)

        data = {'refresh': refresh_token}
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class MeAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserNoPSerializer

    @swagger_auto_schema(
        operation_summary="Получение данных о текущем аккаунте",
        operation_description="Только авторизованные пользователи"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_object(self):
        return self.request.user
    
class GetPostAccounts(APIView):
    permission_classes = [IsAdminUser]
    
    @swagger_auto_schema(
        operation_summary="Получение списка всех аккаунтов",
        operation_description="Только администраторы",
        manual_parameters=[
            openapi.Parameter(
                'from',
                openapi.IN_QUERY,
                description="начало выборки",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'count',
                openapi.IN_QUERY,
                description="размер выборки",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
        ],
        responses={
            200: UserNoPSerializer(many=True),
        }
    )
    def get(self, request):
        queryset = User.objects.exclude(is_superuser=True)
        from_p = int(request.GET.get('from', 1))
        count_p = int(request.GET.get('count', queryset.__len__()))
        queryset = User.objects.exclude(is_superuser=True)[from_p-1:from_p + count_p-1]
        serializer = UserNoPSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Создание администратором нового аккаунта",
        operation_description="Только администраторы",
        request_body=UserRolesSerializer,
        responses={
            201: UserRolesSerializer(many=True),
        }
    )
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
    
    http_method_names = ['put', 'delete']
    
    @swagger_auto_schema(
        operation_summary="Изменение администратором аккаунта по id",
        operation_description="Только администраторы"
    )
    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Мягкое удаление аккаунта по id",
        operation_description="Только администраторы"
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance == request.user:
            return Response({"detail": "Вы не можете удалить себя."}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class GetDoctors(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Получение списка докторов",
        operation_description="Только авторизованные пользователи",
        manual_parameters=[
            openapi.Parameter(
                'from',
                openapi.IN_QUERY,
                description="начало выборки",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'count',
                openapi.IN_QUERY,
                description="размер выборки",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
        ],
        responses={
            200: UserNoPSerializer(many=True),
        }
    )
    def get(self, request):
        queryset = User.objects.filter(is_doctor=True)
        from_p = int(request.GET.get('from', 1))
        count_p = int(request.GET.get('count', queryset.__len__()))
        queryset = User.objects.filter(is_doctor=True)[from_p-1:from_p + count_p-1]
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
class GetDoctorsbyID(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_doctor=True)
    
    @swagger_auto_schema(
        operation_summary="Получение информации о докторе по Id",
        operation_description="**У доктора по умолчанию id 3**.Только авторизованные пользователи"
    )
    def get(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
        except Http404:
            raise NotFound("Доктор с указанным ID не найден.")
        return super().get(request, *args, **kwargs)
    
    def get_object(self):
        try:
            obj = super().get_object()
        except Http404:
            raise NotFound("Доктор с указанным ID не найден.")
        return obj

    
