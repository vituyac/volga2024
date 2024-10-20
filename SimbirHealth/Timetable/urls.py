from django.contrib import admin
from django.urls import path, re_path
from .views import *

urlpatterns = [
    re_path(r'^api/Timetable/?$', TimetableCreateAPIView.as_view()),
    re_path(r'^api/Timetable/(?P<pk>\d+)/?$', TimetableUDAPIView.as_view()),
    re_path(r'^api/Timetable/Doctor/(?P<pk>\d+)/?$', TimetableDoctorView.as_view()),
    re_path(r'^api/Timetable/Hospital/(?P<pk>\d+)/?$', TimetableHospitalView.as_view()),
    re_path(r'^api/Timetable/Hospital/(?P<pk>\d+)/Room/(?P<room>\w+)/?$', TimetableHospitalRoomsView.as_view()),
    re_path(r'^api/Timetable/(?P<pk>\d+)/Appointments/?$', TimetableAddAppoRoomsView.as_view()),
    re_path(r'^api/Appointment/(?P<pk>\d+)/?$', DelTicketView.as_view()),  
]