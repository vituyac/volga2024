from django.contrib import admin
from django.urls import path, re_path
from .views import *

urlpatterns = [
    re_path(r'^Timetable/?$', TimetableCreateAPIView.as_view()),
    re_path(r'^Timetable/(?P<pk>\d+)/?$', TimetableUDAPIView.as_view()),
    re_path(r'^Timetable/Doctor/(?P<pk>\d+)/?$', TimetableDoctorView.as_view()),
    re_path(r'^Timetable/Hospital/(?P<pk>\d+)/?$', TimetableHospitalView.as_view()),
    re_path(r'^Timetable/Hospital/(?P<pk>\d+)/Room/(?P<room>\w+)/?$', TimetableHospitalRoomsView.as_view()),
    re_path(r'^Timetable/(?P<pk>\d+)/Appointments/?$', TimetableAddAppoRoomsView.as_view()),
    re_path(r'^Appointment/(?P<pk>\d+)/?$', DelTicketView.as_view()),  
]