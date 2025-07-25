# assignment/permissions.py
from rest_framework.permissions import BasePermission
from accounts.models import RoleChoice

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == RoleChoice.TEACHER

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == RoleChoice.STUDENT