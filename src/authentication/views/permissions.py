from rest_framework import permissions
from rest_framework.request import Request


class AuthenticationPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        model = "authentication"
        if request.method == "GET":
            return request.user.has_perm(f"{model}.view_user")
        if request.method == "DELETE":
            return request.user.has_perm(f"{model}.delete_attendantprofile")
        if request.method == "PATCH":
            return request.user.has_perm(f"{model}.change_user")

        return False
