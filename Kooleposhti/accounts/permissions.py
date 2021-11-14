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
        return IsInstructor.has_permission(request, view)
        
    


class IsStudent(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and \
            request.user.has_role('student')

        # if not super().has_permission(request, view):
        #     return False
        # try:
        #     instructor = request.user.student
        #     return True
        # except:
        #     return False


class IsInstructor(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and \
            request.user.has_role('instructor')
