from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Check if the user is an admin
    """
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return bool(request.user.is_admin)
        return False
