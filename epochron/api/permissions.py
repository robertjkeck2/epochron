from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to view or edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        elif obj.user:
            return obj.user == request.user
        else:
            return False
