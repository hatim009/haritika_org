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

        obj_block = obj.village.block.code

        return obj_block in [user_bock.block.code for user_bock in request.user.assigned_blocks.all()]
    
    def has_create_permission(self, request, view):
        if IsAdmin().has_permission(request, view):
            return True

        obj_block = None
        if 'village' in request.data:
            try:
                obj_block = VillagesDirectory.objects.get(pk = request.data['village']).block.code
            except VillagesDirectory.DoesNotExist:
                return False
        
        if not obj_block:
            return False
        
        return obj_block in [user_bock.block.code for user_bock in request.user.assigned_blocks.all()]
