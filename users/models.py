"""
User model with role-based access control.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Adds role-based access control and additional fields.
    """
    
    class Role(models.TextChoices):
        VIEWER = 'VIEWER', _('Viewer')
        ANALYST = 'ANALYST', _('Analyst')
        ADMIN = 'ADMIN', _('Admin')
    
    # Override email to make it unique and required
    email = models.EmailField(_('email address'), unique=True)
    
    # Role field
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.VIEWER,
        help_text=_('User role determines permissions')
    )
    
    # Override is_active to have better control
    is_active = models.BooleanField(
        default=True,
        help_text=_('Designates whether this user should be treated as active.')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        verbose_name = _('User')
        verbose_name_plural = _('Users')
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_viewer(self):
        """Check if user has Viewer role."""
        return self.role == self.Role.VIEWER
    
    @property
    def is_analyst(self):
        """Check if user has Analyst role."""
        return self.role == self.Role.ANALYST
    
    @property
    def is_admin(self):
        """Check if user has Admin role."""
        return self.role == self.Role.ADMIN
    
    def can_manage_users(self):
        """Check if user can manage other users."""
        return self.is_admin
    
    def can_create_records(self):
        """Check if user can create financial records."""
        return self.is_admin
    
    def can_view_all_records(self):
        """Check if user can view all records (not just own)."""
        return self.role in [self.Role.ANALYST, self.Role.ADMIN]