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
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
import pytz
from django.utils.dateparse import parse_datetime


class TimetableCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsManager]
    serializer_class = TimetableSerializer
    queryset = Timetable.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        doc_id = request.data.get('doctorId')
        hospital_id = request.data.get('hospitalId')
        room_number = request.data.get('room')
        to = request.data.get('to')
        fr = request.data.get('fr')
        try:
            validate_rooms(self, serializer, doc_id, hospital_id, room_number, fr, to, -1)
            return Response(serializer.data, status=201)
        except ValidationError as e:
            raise DRFValidationError({"detail": e.messages[0]})
        
                

class TimetableUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsManager]
    serializer_class = TimetableSerializer
    queryset = Timetable.objects.all()
    
    def put(self, request, pk):
        timetable_instance = self.get_object()
        serializer = self.get_serializer(timetable_instance, data=request.data)
        if serializer.is_valid():
            try:
                doc_id = request.data.get('doctorId')
                hospital_id = request.data.get('hospitalId')
                room_id = request.data.get('room')
                to = request.data.get('to')
                fr = request.data.get('fr')
                if validate_rooms(self, serializer, doc_id, hospital_id, room_id, fr, to, pk) == 1:
                    serializer.save()
                    return Response(serializer.data)
            except ValidationError as e:
                raise DRFValidationError({"detail": e.messages[0]})
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        timetable_instance = self.get_object()
        timetable_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TimetableDoctorView(APIView):
    permission_classes = [IsManager]
    serializer_class = TimetableSerializer
    queryset = Timetable.objects.all()
    
    def get_permissions(self):
        if self.request.method in ['GET']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
    def get(self, request, pk):
        from_param = request.GET.get('from')
        to_param = request.GET.get('to')
        
        timetables = Timetable.objects.filter(doctorId=pk)

        if from_param:
            from_date = parse_datetime(from_param)
            if from_date:
                timetables = timetables.filter(fr__gte=from_date)

        if to_param:
            to_date = parse_datetime(to_param)
            if to_date:
                timetables = timetables.filter(to__lte=to_date)
        
        timetables = timetables.order_by('fr')

        return Response(list(timetables.values()))
    
    def delete(self, request, pk, *args, **kwargs):
        doc_id = pk
        deleted_count, _ = Timetable.objects.filter(doctorId=doc_id).delete()
        if deleted_count > 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "Записи не найдены."},status=status.HTTP_404_NOT_FOUND)
        
class TimetableHospitalView(APIView):
    permission_classes = [IsManager]
    serializer_class = TimetableSerializer
    queryset = Timetable.objects.all()
    
    def get_permissions(self):
        if self.request.method in ['GET']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
    def get(self, request, pk):
        from_param = request.GET.get('from')
        to_param = request.GET.get('to')
        
        timetables = Timetable.objects.filter(hospitalId=pk)

        if from_param:
            from_date = parse_datetime(from_param)
            if from_date:
                timetables = timetables.filter(fr__gte=from_date)

        if to_param:
            to_date = parse_datetime(to_param)
            if to_date:
                timetables = timetables.filter(to__lte=to_date)
        
        timetables = timetables.order_by('fr')

        return Response(list(timetables.values()))
    
    def delete(self, request, pk, *args, **kwargs):
        hospital_id = pk
        deleted_count, _ = Timetable.objects.filter(hospitalId=hospital_id).delete()
        if deleted_count > 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "Записи не найдены."},status=status.HTTP_404_NOT_FOUND)
    
    
class TimetableHospitalRoomsView(generics.ListAPIView):
    serializer_class = TimetableSerializer
    permission_classes=[IsManagerDoctor]
    
    def get_queryset(self):
        hospital_pk = self.kwargs.get('pk')
        room = self.kwargs.get('room')
        queryset = Timetable.objects.filter(hospitalId=hospital_pk, room=room)
        
        from_param = self.request.GET.get('from')
        to_param = self.request.GET.get('to')

        if from_param:
            from_date = parse_datetime(from_param)
            if from_date:
                queryset = queryset.filter(fr__gte=from_date)

        if to_param:
            to_date = parse_datetime(to_param)
            if to_date:
                queryset = queryset.filter(to__lte=to_date)
        
        queryset = queryset.order_by('fr')
        
        return queryset
    
class TimetableAddAppoRoomsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        timetable = Timetable.objects.filter(id=pk).first()
        
        if not timetable:
            return Response({"detail": "Расписание не найдено."}, status=status.HTTP_404_NOT_FOUND)

        from_time = timetable.fr
        to_time = timetable.to

        available_slots = []
        current_time = from_time

        while current_time < to_time:
            is_booked = Ticket.objects.filter(timetableId=timetable, time=current_time).exists()
            if not is_booked:
                available_slots.append(current_time.isoformat() + 'Z')
            current_time += timedelta(minutes=30)

        return Response(available_slots, status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            time = request.data.get('time')
            time = datetime.fromisoformat(time.replace("Z", "+00:00"))

            if time.second != 0 or time.second != 0:
                return Response({"detail": "Секунды должны быть равны 0."}, status=status.HTTP_400_BAD_REQUEST)
            
            if time.minute % 30 != 0 or time.minute % 30 != 0:
                return Response({"detail": "Минуты должны быть кратны 30."}, status=status.HTTP_400_BAD_REQUEST)
            
            timetable = Timetable.objects.filter(id=pk).first()
            if not timetable:
                return Response({"detail": "Расписание не найдено."}, status=status.HTTP_400_BAD_REQUEST)

            if time < timetable.fr or time > timetable.to:
                return Response({"detail": "Время должно быть в пределах времени приёма."}, status=status.HTTP_400_BAD_REQUEST)

            if Ticket.objects.filter(timetableId=timetable, time=time).exists():
                return Response({"detail": "Это время уже занято."}, status=status.HTTP_400_BAD_REQUEST)
            
            user = request.user
            serializer.save(timetableId=timetable, user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DelTicketView(generics.DestroyAPIView):
    queryset=Ticket.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if request.user.is_authenticated:
            if (instance.user != request.user and not request.user.is_manager and not request.user.is_staff and not request.user.is_superuser):
                return Response({"detail": "У вас недостаточно прав для выполнения данного действия."}, status=status.HTTP_403_FORBIDDEN)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "Учётные данные не предоставлены."}, status=status.HTTP_403_FORBIDDEN)
    
    
def validate_rooms(self, serializer, doc_id, hospital_id, room_number, fr, to, command):
    doctor = User.objects.filter(id=doc_id).first()
    if doctor and doctor.is_doctor == 1:
        hospital = Hospital.objects.filter(id=hospital_id).first()
        if hospital:
            room = Room.objects.filter(hospital=hospital_id, number=room_number).first()
            if room:
                try:
                    validate_dates(fr, to, hospital_id, room_number, command)
                    if command == -1:
                        self.perform_create(serializer)
                    else:
                        return 1
                    return Response(serializer.data, status=201)
                except ValidationError as e:
                    raise DRFValidationError({"detail": e.messages[0]})
            else:
                raise NotFound(f"Кабинет с номером {room_number} в больнице с id {hospital_id} не найден.")
        else:
            raise NotFound(f"Больница с id {hospital_id} не найден.")
    else:
        raise NotFound(f"Доктор с id {doc_id} не найден.")


def validate_dates(fr, to, hospital_id, room_number, command):
    fr_dt = datetime.fromisoformat(fr.replace("Z", "+00:00"))
    to_dt = datetime.fromisoformat(to.replace("Z", "+00:00"))

    if command == -1:
        time_tables = Timetable.objects.filter(hospitalId=hospital_id, room=room_number)
    else:
        time_tables = Timetable.objects.filter(hospitalId=hospital_id, room=room_number).exclude(id=command)

    if fr_dt.second != 0 or to_dt.second != 0:
        raise ValidationError("Секунды должны быть равны 0.")
    
    if fr_dt.minute % 30 != 0 or to_dt.minute % 30 != 0:
        raise ValidationError("Минуты должны быть кратны 30.")

    if to_dt <= fr_dt:
        raise ValidationError("Дата 'to' должна быть больше даты 'from'.")

    diff = to_dt - fr_dt
    if diff > timedelta(hours=12):
        raise ValidationError("Разница между 'to' и 'from' не должна превышать 12 часов.")
    
    fr_dt = fr_dt.astimezone(pytz.UTC)
    to_dt = to_dt.astimezone(pytz.UTC)
    
    for timetable in time_tables:
        if timetable.fr < to_dt and timetable.to > fr_dt:
            raise ValidationError("Выбранное время пересекается с уже существующим расписанием.")
    