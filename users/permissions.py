from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from .models import User


class IsAdmin(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user.user_type == User.UserType.ADMIN
    
    def has_object_permission(self, request, view, obj):
        return request.user.user_type == User.UserType.ADMIN


class IsSupervisor(BasePermission):
    """
    Allows access only to supervisors.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.user_type != User.UserType.SUPERVISOR or obj.user_type == User.UserType.ADMIN:
            return False

        is_self = IsSelf().has_object_permission(request, view, obj)
        has_block_permission = any(user_block.block.code in [obj_block.block.code for obj_block in obj.assigned_blocks.all()] for user_block in request.user.assigned_blocks.all())

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
