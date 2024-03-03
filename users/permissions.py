from rest_framework.permissions import BasePermission

from users.models import User


class IsAdmin(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user.user_type == User.UserType.ADMIN
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsSupervisor(BasePermission):
    """
    Allows access only to supervisors.
    """
    def has_permission(self, request, view):
        return view.action != 'create' and request.user.user_type == User.UserType.SUPERVISOR
 
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
            case 'profile':
                return is_self

        return False
    

class IsSurveyor(BasePermission):
    """
    Allows access only to surveyors.
    """
    def has_permission(self, request, view):
        return view.action != 'create' and request.user.user_type == User.UserType.SURVEYOR
 
    def has_object_permission(self, request, view, obj):
        if not self.has_permission(request, view):
            return False

        is_self = IsSelf().has_object_permission(request, view, obj)

        match view.action:
            case 'retrieve':
                return is_self
            case 'password':
                return is_self
            case 'profile':
                return is_self
            case 'partial_update':
                return is_self
        
        return False


class IsSelf(BasePermission):
    """
    Allows access only to self.
    """

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj)


class HasBlockPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if IsAdmin().has_permission(request, view):
            return True

        obj_blocks = [user_block.block.code for user_block in obj.assigned_blocks.all()]

        return any(user_bock.block.code in obj_blocks for user_bock in request.user.assigned_blocks.all())
