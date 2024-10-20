from django.shortcuts import render
from .models import *
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
from Account.permissions import IsManager, IsManagerDoctor
from Hospital.models import Hospital, Room
from Account.models import User
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import pytz
from django.utils.dateparse import parse_datetime

class GetHistoryView(generics.ListAPIView):
    serializer_class = HistorySerializer

    @swagger_auto_schema(
        operation_summary="Получение истории посещений и назначений аккаунта",
        operation_description="Возвращает записи где {pacientId}={id}. Только врачи и аккаунт, которому принадлежит история",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return History.objects.none()
        
        pk = int(self.kwargs.get('pk'))

        if not self.request.user.is_authenticated:
            raise NotAuthenticated("Учётные данные не предоставлены.")
        
        if pk == self.request.user.id or self.request.user.is_doctor:
            queryset = History.objects.filter(pacientId=pk)
            return queryset
        else:
            raise PermissionDenied("У вас недостаточно прав для выполнения данного действия.")
        
class HistoryRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsManagerDoctor]
    serializer_class = HistorySerializer
    queryset = History.objects.all()
    
    http_method_names = ['get', 'put']
    
    def get_permissions(self):
        if self.request.method in ['GET']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
    @swagger_auto_schema(
        operation_summary="Получение подробной информации о посещении и назначениях",
        operation_description="Только врачи и аккаунт, которому принадлежит история",
    )
    def get(self, request, pk, *args, **kwargs):
        
        queryset = History.objects.filter(id=pk).first()
        
        if queryset.pacientId_id == request.user.id or request.user.is_doctor:
            serializer = HistorySerializer(queryset)
            return Response(serializer.data)
        else:
            raise PermissionDenied("У вас недостаточно прав для выполнения данного действия.")
        
    @swagger_auto_schema(
        operation_summary="Обновление истории посещения и назначения",
        operation_description="Только администраторы и менеджеры и врачи. {pacientId} - с ролью User",
    )
    def put(self, request, pk):
        history_instance = self.get_object()
        serializer = self.get_serializer(history_instance, data=request.data)
        if serializer.is_valid():
            try:
                pacient_id = request.data.get('pacientId')
                doc_id = request.data.get('doctorId')
                hospital_id = request.data.get('hospitalId')
                room_number = request.data.get('room')
                date = request.data.get('date')
                data = request.data.get('data')
                
                if validate_rooms(self, serializer, doc_id, hospital_id, pacient_id, room_number, 1) == 1:
                    serializer.save()
                    return Response(serializer.data)
            except ValidationError as e:
                raise DRFValidationError({"detail": e.messages[0]})
        return Response(serializer.errors, status=400)


class HistoryCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsManagerDoctor]
    serializer_class = HistorySerializer
    queryset = History.objects.all()
        
    
    @swagger_auto_schema(
        operation_summary="Создание истории посещения и назначения",
        operation_description="Только администраторы и менеджеры и врачи. {pacientId} - с ролью User",
        responses={201: HistorySerializer},
        request_body=HistorySerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        pacient_id = request.data.get('pacientId')
        doc_id = request.data.get('doctorId')
        hospital_id = request.data.get('hospitalId')
        room_number = request.data.get('room')
        date = request.data.get('date')
        data = request.data.get('data')
        
        try:
            validate_rooms(self, serializer, doc_id, hospital_id, pacient_id, room_number, 0)
            return Response(serializer.data, status=201)
        except ValidationError as e:
            raise DRFValidationError({"detail": e.messages[0]})
        
def validate_rooms(self, serializer, doc_id, hospital_id, pacient_id, room_number, command):
    doctor = User.objects.filter(id=doc_id).first()
    if doctor and doctor.is_doctor == 1:
        hospital = Hospital.objects.filter(id=hospital_id).first()
        if hospital:
            pacient = User.objects.filter(id=pacient_id).first()
            if pacient:
                room = Room.objects.filter(hospital=hospital_id, number=room_number).first()
                if room:
                    try:
                        if command == 0:
                            self.perform_create(serializer)
                        else:
                            return 1
                        return Response(serializer.data, status=201)
                    except ValidationError as e:
                        raise DRFValidationError({"detail": e.messages[0]})
                else:
                    raise NotFound(f"Кабинет с номером {room_number} в больнице с id {hospital_id} не найден.")
            else:
                raise NotFound(f"Пациент с id {pacient_id} не найден.")
        else:
            raise NotFound(f"Больница с id {hospital_id} не найдена.")
    else:
        raise NotFound(f"Доктор с id {doc_id} не найден.")
