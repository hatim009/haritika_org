from rest_framework.permissions import BasePermission
from users.models import User

from local_directories.models import VillagesDirectory


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
        if view.action == 'create':
            return request.user.user_type == User.UserType.SUPERVISOR and HasBlockPermission().has_create_permission(request, view)       
        
        return request.user.user_type == User.UserType.SUPERVISOR

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view) and HasBlockPermission().has_object_permission(request, view, obj)
    

class IsSurveyor(BasePermission):
    """
    Allows access only to surveyors.
    """
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.user_type == User.UserType.SURVEYOR and HasBlockPermission().has_create_permission(request, view)
        
        return request.user.user_type == User.UserType.SURVEYOR

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view) and HasBlockPermission().has_object_permission(request, view, obj)


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
    
    def has_create_permission(self, request, view):
        if IsAdmin().has_permission(request, view):
            return True

        obj_blocks = None
        if 'village' in request.data:
            obj_blocks = VillagesDirectory.objects.get(pk = request.data['village']).block.code
        if 'block' in request.data:
            obj_blocks = request.data['block']

        if not obj_blocks:
            return False
        
        return any(user_block.block.code == obj_blocks for user_block in request.user.assigned_blocks.all())


class HasParentsBlockPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        parent_obj = getattr(obj, view.get_serializer.Meta.parent_attribute)
        return HasBlockPermission().has_object_permission(request, view, parent_obj)
    
    def has_create_permission(self, request, view):
        return True