from rest_framework.permissions import IsAdminUser, IsAuthenticated, BasePermission
from rest_framework import permissions


class IsAdminOrReadOnly(BasePermission):
    # is_staff -> can login to admin panel
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and
                    request.user.is_staff  # admin user
                    )
