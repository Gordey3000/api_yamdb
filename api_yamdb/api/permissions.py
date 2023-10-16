from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


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
        if request.method == 'GET':
            return True
        elif request.method in ['HEAD', 'OPTIONS']:
            return True
        elif request.method == 'DELETE':
            return request.user.is_authenticated and request.user.is_admin
        else:
            return request.user.is_authenticated


class IsAdminOrPostOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated and request.user.is_admin
        elif request.method == 'DELETE':
            return request.user.is_authenticated and request.user.is_admin
        return (
            request.method in SAFE_METHODS
            or request.user and request.user.is_superuser
        )
