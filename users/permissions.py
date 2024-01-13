from rest_framework.permissions import BasePermission

from users.models import User
from permissions import HasBlockPermission


class IsSupervisor(BasePermission):
    """
    Allows access only to supervisors.
    """
    def has_permission(self, request, view):
        return request.user.user_type == User.UserType.SURVEYOR
 
    def has_object_permission(self, request, view, obj):
        if not self.has_permission(request, view) or obj.user_type == User.UserType.ADMIN:
            return False

        is_self = IsSelf().has_object_permission(request, view, obj)
        has_block_permission = HasBlockPermission().has_object_permission(request, view, obj)

        match view.action:
            case 'partial_update':
                """Supervisor is only allowed to assign projects to users"""
                if len(request.data) > 1 or 'projects' not in request.data:
                    return False
                return has_block_permission
            case 'retrieve':
                return has_block_permission
            case 'password':
                return is_self

        return False
    

class IsSurveyor(BasePermission):
    """
    Allows access only to surveyors.
    """
    def has_permission(self, request, view):
        return request.user.user_type == User.UserType.SURVEYOR
 
    def has_object_permission(self, request, view, obj):
        if request.user.user_type != User.UserType.SURVEYOR or obj.user_type != User.UserType.SURVEYOR:
            return False

        is_self = IsSelf().has_object_permission(request, view, obj)

        match view.action:
            case 'retrieve':
                return is_self
            case 'password':
                return is_self
            
        return False


class IsSelf(BasePermission):
    """
    Allows access only to self.
    """

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj)
