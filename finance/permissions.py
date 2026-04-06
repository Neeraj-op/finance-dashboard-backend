"""
Permissions for Financial Records.
"""
from rest_framework import permissions


class CanCreateRecord(permissions.BasePermission):
    """Only Admin can create financial records."""
    message = 'Only administrators can create financial records.'
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Allow GET for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow POST, PUT, PATCH, DELETE only for admins
        return request.user.role == 'ADMIN'


class CanViewAllRecords(permissions.BasePermission):
    """Analysts and Admins can view all records."""
    message = 'Only analysts and administrators can view all records.'
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        return request.user.role in ['ANALYST', 'ADMIN']