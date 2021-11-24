from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticatedOrReadOnly


class IsEmployerOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_employer


class IsCompanyEmployerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return user.is_authenticated and user.is_employer and obj.employer == user
