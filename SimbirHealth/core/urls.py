from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Account.urls')),
    path('api/', include('Hospital.urls')),
    path('api/', include('Timetable.urls')),
    path('api/', include('Document.urls')),
    path('document/', include('Document.swagger')),
    path('account/', include('Account.swagger')),
    path('hospital/', include('Hospital.swagger')),
    path('timetable/', include('Timetable.swagger')),
]
