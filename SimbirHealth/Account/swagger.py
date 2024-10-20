from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import urls as app_urls
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import authentication

schema_view = get_schema_view(
    openapi.Info(
        title="Account API",
        default_version='v1',
        description="API documentation for Account service",
    ),
    patterns=app_urls.urlpatterns,
    authentication_classes=(authentication.BasicAuthentication,),
    public=True,
)

urlpatterns = [
    path('ui-swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]