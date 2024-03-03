from rest_framework.permissions import BasePermission
from users.models import User

from land_parcels.models import LandParcel
from .models import CarbonSequestration


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
        if view.action == 'create':
            return request.user.user_type == User.UserType.SUPERVISOR and HasProjectPermission().has_create_permission(request, view)       
        
        return request.user.user_type == User.UserType.SUPERVISOR

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view) and HasProjectPermission().has_object_permission(request, view, obj)
    

class IsSurveyor(BasePermission):
    """
    Allows access only to surveyors.
    """
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.user_type == User.UserType.SURVEYOR and HasProjectPermission().has_create_permission(request, view)
        
        return request.user.user_type == User.UserType.SURVEYOR

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view) and HasProjectPermission().has_object_permission(request, view, obj)


class HasProjectPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if IsAdmin().has_permission(request, view):
            return True

        if (not hasattr(obj, 'PROJECT_ID')):
            return False
        
        project_id = obj.PROJECT_ID
        assigned_blocks = [user_project_block.block.code for user_project_block in request.user.assigned_projects.all() if project_id == user_project_block.project.id]

        if not assigned_blocks:
            return False
        
        obj_block = obj.land_parcel.village.block.code

        return obj_block in assigned_blocks
    

    def has_create_permission(self, request, view):
        if IsAdmin().has_permission(request, view):
            return True

        assigned_blocks = [user_project_block.block.code for user_project_block in request.user.assigned_projects.all() if CarbonSequestration.PROJECT_ID == user_project_block.project.id]

        if not assigned_blocks:
            return False
        
        obj_block = None
        if 'land_parcel' in request.data:
            try:
                obj_block = LandParcel.objects.get(pk = request.data['land_parcel']).village.block.code
            except LandParcel.DoesNotExist:
                return False
        
        if not obj_block:
            return False
        
        return obj_block in assigned_blocks
