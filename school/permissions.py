from rest_framework.permissions import BasePermission

from accounts.models import RoleChoice


class IsAuthenticatedInTenant(BasePermission):
    """Base class that ensures user is authenticated and in correct tenant"""
    def has_permission(self, request, view):
        return request.user.is_authenticated  # Your middleware handles tenant


class IsPrincipal(IsAuthenticatedInTenant):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == RoleChoice.PRINCIPAL