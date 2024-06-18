from rest_framework.permissions import BasePermission, SAFE_METHODS

from nft_app.models import User


class IsSalesmanOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        return bool(
            request.method in SAFE_METHODS or
            request.user.role == User.SALESMAN or
            request.user.is_superuser
        )


class IsAdminUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user.role == User.ADMIN or
            request.user.is_superuser
        )


class IsSalesman(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == User.SALESMAN or request.user.is_superuser
    

class IsOwnerProductOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
            return bool(
            request.method in SAFE_METHODS or
            request.user == obj.user or
            request.user.is_superuser
        )


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
            return bool(
            request.method in SAFE_METHODS or
            request.user == obj.user or
            request.user.is_superuser
        )
    