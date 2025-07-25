from rest_framework.permissions import BasePermission
from rolepermissions.checkers import has_permission
from rolepermissions.roles import get_user_roles

class HasDashboardPermission(BasePermission):
    def has_permission(self, request, view):

        required_permission = getattr(view, 'required_permission', None)
        print("required", required_permission)
        print("This is request.user", request.user)
        print("This is all permissions",request.user.get_all_permissions())

        print("Dashboard",has_permission(request.user, required_permission))
        print("principal role",get_user_roles(request.user))

        print("Dashboard Request User", request.user)
        # Explicitly deny access if no permission is specified
        if not required_permission:
            return False

        return has_permission(request.user, required_permission)