from rest_framework.permissions import BasePermission
from Timetable.models import *

class IsManager(BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.is_manager or request.user.is_staff or request.user.is_superuser
        return False
    
class IsManagerDoctor(BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.is_manager or request.user.is_staff or request.user.is_superuser or request.user.is_doctor
        return False
    