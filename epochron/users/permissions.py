from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to view or edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        elif obj.id:
            return obj.id == request.user.id
        else:
            return False
