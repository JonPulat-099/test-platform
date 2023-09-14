from rest_framework import permissions


class StudentOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'is_student')
