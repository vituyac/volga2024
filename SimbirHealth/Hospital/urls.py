from django.contrib import admin
from django.urls import path, re_path
from .views import *

urlpatterns = [
    re_path(r'^Hospitals/?$', GetPostHospitals.as_view()),
    re_path(r'^Hospitals/(?P<pk>\d+)/?$', GetPutHospital.as_view()),
    re_path(r'^Hospitals/(?P<pk>\d+)/Rooms/?$', GetHospitalsRoom.as_view()),
    
    
    #re_path(r'^Doctors/(?P<pk>\d+)/?$', GetDoctorsbyID.as_view()),
    
    
]