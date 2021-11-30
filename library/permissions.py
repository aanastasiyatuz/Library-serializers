from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

User = get_user_model()

class IsAdminPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not isinstance(user, User): return False
        return bool(request.user.group.lower()=='admin')
