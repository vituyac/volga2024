from django.contrib import admin
from django.urls import path, include
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import urls as app_urls
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import authentication


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Account.urls')),
    path('', include('Hospital.urls')),
    path('', include('Timetable.urls')),
    path('', include('Document.urls')),
    path('account/', include('Account.swagger')),
    path('hospital/', include('Hospital.swagger')),
    path('timetable/', include('Timetable.swagger')),
    path('document/', include('Document.swagger')),
]
