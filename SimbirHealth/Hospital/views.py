from django.shortcuts import render
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
from drf_yasg import openapi

class GetPostHospitals(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['POST']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    @swagger_auto_schema(
        operation_summary="Получение списка больниц",
        operation_description="У Rooms - тип данных string, но возвращается список кабинетов (особенности swagger)\nТолько авторизованные пользователи",
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
            200: HospitalSerializer(many=True),
        }
    )
    def get(self, request):
        queryset = Hospital.objects.all()
        from_p = int(request.GET.get('from', 1))
        count_p = int(request.GET.get('count', queryset.__len__()))
        queryset = Hospital.objects.all()[from_p-1:from_p + count_p-1]
        serializer = HospitalSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Создание записи о новой больнице",
        operation_description="Список кабинетов: если не указан или пустой - кабинеты отсутствуют\nТолько администраторы",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    title="Name",
                    maxLength=255,
                    minLength=1,
                    description="Название больницы (обязательное поле)"
                ),
                'address': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    title="Address",
                    maxLength=255,
                    minLength=1,
                    description="Адрес больницы (обязательное поле)"
                ),
                'contactPhone': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    title="ContactPhone",
                    maxLength=255,
                    minLength=1,
                    description="Контактный телефон (обязательное поле)"
                ),
                'rooms': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Список кабинетов. Если не указан или пустой - кабинеты отсутствуют"
                    ),
                    title="Rooms",
                )
            },
            required=['name', 'address', 'contactPhone'],
            description="Создание записи о новой больнице"
        ),
    )
    def post(self, request):
        serializer = HospitalSerializer(data=request.data)
        if serializer.is_valid():
            hospital_instance = serializer.save()
            rooms = request.data.get('rooms')
            if rooms:
                for room in rooms:
                    Room.objects.create(
                        hospital=hospital_instance,
                        number=room
                    )
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
class GetPutHospital(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HospitalSerializer
    queryset = Hospital.objects.all()
    
    http_method_names = ['get', 'put', 'delete']
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    
    
    @swagger_auto_schema(
        operation_summary="Получение информации о больнице по Id",
        operation_description="У Rooms - тип данных string, но возвращается список кабинетов (особенности swagger)\nТолько авторизованные пользователи",
    )
    def get(self, request, pk):
        hospital_instance = self.get_object()
        serializer = self.get_serializer(hospital_instance)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Изменение информации о больнице по Id",
        operation_description="Список кабинетов: если не указан - список не меняется, если пустой - все кабинеты удаляются, если не пустой - список кабинетов заменяется на новый\nТолько администраторы",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    title="Name",
                    maxLength=255,
                    minLength=1,
                    description="Название больницы (обязательное поле)"
                ),
                'address': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    title="Address",
                    maxLength=255,
                    minLength=1,
                    description="Адрес больницы (обязательное поле)"
                ),
                'contactPhone': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    title="ContactPhone",
                    maxLength=255,
                    minLength=1,
                    description="Контактный телефон (обязательное поле)"
                ),
                'rooms': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Список кабинетов (Если не указан - список не меняется, если пустой - все кабинеты удаляются, если не пустой - список кабинетов заменяется на новый)"
                    ),
                    title="Rooms",
                )
            },
            required=['name', 'address', 'contactPhone'],
            description="Создание записи о новой больнице"
        ),
    )
    def put(self, request, pk):
        hospital_instance = self.get_object()
        serializer = self.get_serializer(hospital_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            rooms = request.data.get('rooms')
            if (rooms != None and rooms == []):
                queryset = Room.objects.filter(hospital=hospital_instance)
                for room in queryset:
                    room.delete()
            if rooms:
                for room in rooms:
                    r = Room.objects.filter(hospital=hospital_instance, number=room)
                    if not r:
                        Room.objects.create(
                            hospital=hospital_instance,
                            number=room
                        )
                if (len(Room.objects.filter(hospital=hospital_instance)) != len(rooms)):
                    queryset = Room.objects.filter(hospital=hospital_instance)
                    for room in queryset:
                        if (not(room.number in rooms)):
                            room.delete()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    @swagger_auto_schema(
        operation_summary="Мягкое удаление записи о больнице",
        operation_description="Только администраторы",
    )
    def delete(self, request, pk):
        hospital_instance = self.get_object()
        hospital_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
    
class GetHospitalsRoom(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Получение списка кабинетов больницы по Id",
        operation_description="Только авторизованные пользователи",
        responses={
            200: "Список кабинетов",
        }
    )
    def get(self, request, pk):
        rooms = Room.objects.filter(hospital=pk)
        room_numbers = rooms.values_list('number', flat=True)
        return Response(list(room_numbers))
    
        
        
    