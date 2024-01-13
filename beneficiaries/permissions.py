from rest_framework.permissions import BasePermission
from users.models import User
from permissions import HasParentsBlockPermission


class IsSupervisor(BasePermission):
    """
    Allows access only to supervisors.
    """
    def has_permission(self, request, view):
        return request.user.user_type == User.UserType.SUPERVISOR
    
    def has_object_permission(self, request, view, obj):
        if not self.has_permission(request, view):
            return False
        
        return HasParentsBlockPermission().has_object_permission(request, view, obj)
    

class IsSurveyor(BasePermission):
    """
    Allows access only to surveyors.
    """
    def has_permission(self, request, view):
        return request.user.user_type == User.UserType.SURVEYOR
    
    def has_object_permission(self, request, view, obj):
        if not self.has_permission(request, view):
            return False
        
        return HasParentsBlockPermission().has_object_permission(request, view, obj)

