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

class IsInstructorOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        try: 
            if super().has_permission(request, view):
                instructor = request.user.instructor
                return True
        except: return False 

class IsStudent(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and bool(request.user.student)

class IsInstructor(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and bool(request.user.instructor)
