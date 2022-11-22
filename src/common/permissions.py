from rest_framework import permissions


class AdminBasePermission(permissions.BasePermission):
    message = "Admin does not have permission to perform this action / to access this resource."

    def has_permission(self, request, view):
        pass


class AttendantBasePermission(permissions.BasePermission):
    message = "Attendant does not have permission to perform this action / to access this resource."

    def has_permission(self, request, view):
        pass
