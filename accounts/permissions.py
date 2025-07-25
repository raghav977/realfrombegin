from rest_framework.permissions import BasePermission

from rolepermissions.checkers import has_role
from rolepermissions.roles import get_user_roles
from icecream import ic


from rolepermissions.checkers import has_role
from rolepermissions.roles import get_user_roles



from accounts.models import RoleChoice

from section.models import ClassTeacher
class IsAuthenticatedInTenant(BasePermission):
    """Base class that ensures user is authenticated and in correct tenant"""
    def has_permission(self, request, view):
        return request.user.is_authenticated  # Your middleware handles tenant


# Concrete role permissions
class IsAdmin(IsAuthenticatedInTenant):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == RoleChoice.ADMIN


class IsModerator(IsAuthenticatedInTenant):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == RoleChoice.MODERATOR


class IsTeacher(IsAuthenticatedInTenant):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == RoleChoice.TEACHER


class IsStudent(IsAuthenticatedInTenant):
    def has_permission(self, request, view):

        print("This is user role",request.user.role) 
        role = get_user_roles(request.user)
        ic("These are roles",role)


        print("This is user role",request.user.role) 
        role = get_user_roles(request.user)
        ic("These are roles",role)

        print("This is role",RoleChoice.PRINCIPAL) 
        # print("This is has role",has_role(request.user,'principal'))
        # print("This is role",)
        return (
            
            request.user.is_authenticated
            and (request.user.role == RoleChoice.PRINCIPAL)
            # and has_role(request.user, 'principal')
        )

        


class IsPrincipal(IsAuthenticatedInTenant):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == RoleChoice.PRINCIPAL


class IsSchoolStaff(IsAuthenticatedInTenant):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.role == RoleChoice.TEACHER)
            and has_role(request.user, 'teacher')
        )


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and (
            request.user.role == RoleChoice.TEACHER or
            request.user.role == RoleChoice.PRINCIPAL
        )


class IsStaffOrPrincipal(BasePermission):
    """Allows access to staff members and yprincipals."""

    def has_permission(self, request, view):
        return super().has_permission(request, view) and (
            request.user.role == RoleChoice.STAFF or
            request.user.role == RoleChoice.ADMIN or 
            request.user.role == RoleChoice.PRINCIPAL
        )

class IsStaffOrPrincipal(IsAuthenticatedInTenant):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and (
            request.user.role == RoleChoice.STAFF or
            request.user.role == RoleChoice.PRINCIPAL)


class IsClassTeacher(IsAuthenticatedInTenant):
    def has_permission(self,request,view):
        user = request.user
        
        class_teacher = ClassTeacher.objects.filter(teacher__user=user).exists()
        if class_teacher:
            return True
        else:
            return False