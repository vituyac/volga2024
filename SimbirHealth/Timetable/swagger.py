from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import urls as app_urls

schema_view = get_schema_view(
    openapi.Info(
        title="Timetable API",
        default_version='v1',
        description="API documentation for Timetable service",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=app_urls.urlpatterns
)

urlpatterns = [
    path('ui-swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]