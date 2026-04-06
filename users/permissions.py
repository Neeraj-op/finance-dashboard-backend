"""
Custom permission classes for role-based access control.
"""
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Permission class for Admin-only access.
    """
    message = 'Only administrators can perform this action.'
    
    def has_permission(self, request, view):
        """Check if user is authenticated and has Admin role."""
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'ADMIN'
        )


class IsAnalyst(permissions.BasePermission):
    """
    Permission class for Analyst and above (Analyst + Admin).
    """
    message = 'Only analysts and administrators can perform this action.'
    
    def has_permission(self, request, view):
        """Check if user is Analyst or Admin."""
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in ['ANALYST', 'ADMIN']
        )


class IsViewer(permissions.BasePermission):
    """
    Permission class for any authenticated user (Viewer + Analyst + Admin).
    """
    message = 'Authentication required.'
    
    def has_permission(self, request, view):
        """Check if user is authenticated."""
        return request.user and request.user.is_authenticated


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission: owner of the object or Admin.
    """
    message = 'You can only access your own records.'
    
    def has_object_permission(self, request, view, obj):
        """Check if user owns the object or is Admin."""
        # Admins can access any object
        if request.user.role == 'ADMIN':
            return True
        
        # Check if object has a user field
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # For User objects, check if it's the same user
        if hasattr(obj, 'id') and hasattr(request.user, 'id'):
            return obj.id == request.user.id
        
        return False


class ReadOnlyOrAdmin(permissions.BasePermission):
    """
    Read-only for non-admins, full access for admins.
    """
    message = 'Only administrators can modify this resource.'
    
    def has_permission(self, request, view):
        """Allow read for authenticated, write for admins."""
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Allow read operations (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow write operations only for admins
        return request.user.role == 'ADMIN'