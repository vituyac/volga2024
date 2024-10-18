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
import pytz
from django.utils.dateparse import parse_datetime

class GetHistoryView(generics.ListAPIView):
    serializer_class = HistorySerializer

    def get_queryset(self):
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
    
    def get_permissions(self):
        if self.request.method in ['GET']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
    def get(self, request, pk, *args, **kwargs):
        
        queryset = History.objects.filter(id=pk).first()
        
        if queryset.pacientId_id == request.user.id or request.user.is_doctor:
            serializer = HistorySerializer(queryset)
            return Response(serializer.data)
        else:
            raise PermissionDenied("У вас недостаточно прав для выполнения данного действия.")
        
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
        
    
    def create(self, request, *args, **kwargs):
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
