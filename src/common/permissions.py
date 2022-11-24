import typing as tp
from rest_framework import permissions
from django.contrib.auth.models import Permission, Group


class CustomBasePermission(permissions.BasePermission):
    def get_user_permissions(self, user):
        return Permission.objects.filter(user=user)

    def get_user_groups(self, user) -> tp.List[Group]:
        return [g for g in user.groups.all()]


class AdminBasePermission(permissions.BasePermission):
    message = "Admin does not have permission to perform this action / to access this resource."

    def has_permission(self, request, view):
        ...


class AttendantBasePermission(permissions.BasePermission):
    message = "Attendant does not have permission to perform this action / to access this resource."

    def has_permission(self, request, view):
        ...


class BlocklistPermission(permissions.BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_permission(self, request, view):
        ...
        # ip_addr = request.META['REMOTE_ADDR']
        # blocked = Blocklist.objects.filter(ip_addr=ip_addr).exists()
        # return not blocked
