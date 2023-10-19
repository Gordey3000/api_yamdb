from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
# from reviews.models import User


'''class IsAdminOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_admin
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_admin
            or request.user.is_staff
        )'''


class IsAdminOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin
                     or request.user.role == 'ADMIN'))

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and (request.user.is_admin
                 or request.user.role == 'ADMIN' or request.user.is_staff)
        )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user and request.user.is_superuser
            or request.user.is_authenticated
        )


class AuthorIsAuthenticatedModeratorAdminSuperuserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user or request.user.is_moderator
            or request.user.is_admin or request.user.is_superuser)
