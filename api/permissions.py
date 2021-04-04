import logging

from rest_framework import permissions

from users.models import Role

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)


class IsAdminPermission(permissions.BasePermission):
    """Custom permission to only allow owners of an object to edit it."""
    admin_role = Role.ADMIN

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_staff
        )

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_staff
        )


class IsModeratorPermission(permissions.BasePermission):
    """Custom permission to allow moderator do need actions."""
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.is_moderator
        )


class IsUserPermission(permissions.BasePermission):
    """Custom permission to allow user do need actions."""
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.is_user
        )


class IsSuperUserOrReadOnlyPermission(permissions.BasePermission):
    """Custom permission for checking acceptable actions for
       super user or allowing actions in safe methods."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser


class AuthorOrManageSiteRolesPermission(permissions.BasePermission):
    """Custom permission of managing objects for
       author, moderator and admin."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            obj.author == request.user
            or (request.user.is_admin or request.user.is_moderator)
        )
