from rest_framework.permissions import BasePermission
from users.models import User


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
    def has_permission(self, request, view):
        return request.user.user_type == User.UserType.SUPERVISOR
    
    def has_object_permission(self, request, view, obj):
        if not self.has_permission(request, view):
            return False
        
        return HasBlockPermission().has_object_permission(request, view, obj)
    

class IsSurveyor(BasePermission):
    """
    Allows access only to surveyors.
    """
    def has_permission(self, request, view):
        return request.user.user_type == User.UserType.SURVEYOR
    
    def has_object_permission(self, request, view, obj):
        if not self.has_permission(request, view):
            return False
        
        return HasBlockPermission().has_object_permission(request, view, obj)


class HasBlockPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if IsAdmin().has_permission(request, view):
            return True

        obj_blocks = None
        if hasattr(obj, 'village'):
            obj_blocks = [obj.village.block.code]
        elif hasattr(obj, 'block'):
            obj_blocks = [obj.block.code]
        elif hasattr(obj, 'assigned_blocks'):
            obj_blocks = [obj_block.block.code for obj_block in obj.assigned_blocks.all()]
        
        if not obj_blocks:
            return False

        return any(user_block.block.code in obj_blocks for user_block in request.user.assigned_blocks.all())


class HasParentsBlockPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        parent_obj = getattr(obj, view.get_serializer.Meta.parent_attribute)
        return HasBlockPermission().has_object_permission(request, view, parent_obj)