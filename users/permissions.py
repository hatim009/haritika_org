from rest_framework.permissions import BasePermission
from .models import User



class IsAdmin(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user.user_type == User.UserType.ADMIN)


class IsSupervisor(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user.user_type == User.UserType.SUPERVISOR)
    

class IsSurveyor(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user.user_type == User.UserType.SURVEYOR)


class IsSelf(BasePermission):
    """
    Allows access only to self.
    """

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj)