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


# class IsInstructorOrReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         # return super(IsAuthenticated, IsInstructorOrReadOnly).has_permission(self, request, view) and \
#         return request.user.has_role('instructor')


# class IsStudent(BasePermission):
#     def has_permission(self, request, view):
#         # return super(IsAuthenticated, IsStudent).has_permission(self, request, view) and \
#         return request.user.has_role('student')


# class IsInstructor(BasePermission):
#     def has_permission(self, request, view):
#         # return super(IsAuthenticated, IsInstructor).has_permission(self, request, view) and \
#         return request.user.has_role('instructor')

class IsInstructorOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super().has_permission(request, view) and \
            request.user.has_role('instructor')   


class IsStudent(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and \
            request.user.has_role('student')

class IsInstructor(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and \
            request.user.has_role('instructor')

