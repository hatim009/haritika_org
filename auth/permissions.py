from rest_framework.permissions import BasePermission
from users.models import User


class IsAdmin(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user.user_type == User.UserType.ADMIN)


class IsSupervisor(BasePermission):
    """
    Allows access only to supervisors.
    """

    def has_permission(self, request, view):
        return bool(request.user.user_type == User.UserType.SUPERVISOR)    

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)
    

class IsSurveyor(BasePermission):
    """
    Allows access only to surveyors.
    """

    def has_permission(self, request, view):
        return bool(request.user.user_type == User.UserType.SURVEYOR)


class IsSelf(BasePermission):
    """
    Allows access only to self.
    """

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj)


class IsAdminOrSupervisor(BasePermission):
    def has_permission(self, request, view):
        return bool(IsAdmin().has_permission(request, view)) or bool(IsSupervisor().has_permission())

    def has_object_permission(self, request, view, obj):
        return bool(IsAdmin().has_object_permission(request, view, obj)) or bool(IsSupervisor().has_object_permission(request, view, obj))


class IsAdminOrSelf(BasePermission):
    def has_permission(self, request, view):
        return bool(IsAdmin().has_permission(request, view)) or bool(IsSelf().has_permission())

    def has_object_permission(self, request, view, obj):
        return bool(IsAdmin().has_object_permission(request, view, obj)) or bool(IsSelf().has_object_permission(request, view, obj))


class isSupervisorOrSelf(BasePermission):
    def has_permission(self, request, view):
        return bool(IsSupervisor().has_permission(request, view)) or bool(IsSelf().has_permission())

    def has_object_permission(self, request, view, obj):
        return bool(IsSupervisor().has_object_permission(request, view, obj)) or bool(IsSelf().has_object_permission(request, view, obj))


class hasBlockPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if IsAdmin().has_permission(request, view, obj):
            return True

        curr_block = None
        if hasattr(obj, 'village'):
            curr_block = obj.village.block.code
        elif hasattr(obj, 'block'):
            curr_block = obj.block.code    
        
        if not curr_block:
            return False

        assigned_blocks = [user_block.block.code for user_block in request.user.assigned_blocks.all()]

        if curr_block and curr_block in assigned_blocks:
            return True
        
        return False


class hasParentsBlockPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        parent_obj = getattr(obj, view.get_serializer.Meta.parent_attribute)
        return hasBlockPermission().has_object_permission(request, view, parent_obj)
