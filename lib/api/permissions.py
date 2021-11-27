from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticatedOrReadOnly


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff


class IsEmployerOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_employer


class IsObjectEmployerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user.is_authenticated and user.is_employer)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user.is_authenticated and user.is_employer and obj.employer == user.employer)


class IsEmployer(IsObjectEmployerOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user.is_authenticated and user.is_employer)


class IsEmployerOwnedEmployeeOrReadOnly(IsObjectEmployerOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user.is_authenticated and user.is_employer and obj.company.employer == user.employer)
