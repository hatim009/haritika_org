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
        return request.user.user_type == User.UserType.SUPERVISOR

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
    

class IsSurveyor(BasePermission):
    """
    Allows access only to surveyors.
    """
    def has_permission(self, request, view):
        return request.user.user_type == User.UserType.SURVEYOR

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
