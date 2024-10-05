from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Account.urls')),
    path('api/', include('Hospital.urls')),
    path('api/', include('Timetable.urls')),
]
