from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsJobSeekerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user.is_authenticated and request.user.is_job_seeker)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user.is_authenticated and user.is_job_seeker and obj.job_seeker == user.job_seeker)
