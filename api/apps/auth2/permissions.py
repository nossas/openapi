from rest_framework import permissions

class UsersGroupAuthenticated(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return hasattr(request, 'openapi_group')