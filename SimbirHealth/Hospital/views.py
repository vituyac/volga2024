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

class GetPostHospitals(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['POST']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    def get(self, request):
        queryset = Hospital.objects.all()
        from_p = int(request.GET.get('from', 0))
        count_p = int(request.GET.get('count', queryset.__len__()))
        queryset = Hospital.objects.all()[from_p-1:from_p + count_p-1]
        serializer = HospitalSerializer(queryset, many=True)
        return Response(serializer.data)
    
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
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
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
    
    def delete(self, request, pk):
        hospital_instance = self.get_object()
        hospital_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
    
class GetHospitalsRoom(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        rooms = Room.objects.filter(hospital=pk)
        room_numbers = rooms.values_list('number', flat=True)
        return Response(list(room_numbers))
    
        
        
    