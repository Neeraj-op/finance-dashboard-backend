"""
Django admin configuration for FinancialRecord model.
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import FinancialRecord


@admin.register(FinancialRecord)
class FinancialRecordAdmin(admin.ModelAdmin):
    """Admin for Financial Records."""
    
    list_display = [
        'id',
        'user',
        'amount',
        'type',
        'category',
        'date',
        'is_deleted',
        'created_at'
    ]
    
    list_filter = [
        'type',
        'category',
        'is_deleted',
        'date',
        'created_at'
    ]
    
    search_fields = [
        'user__username',
        'user__email',
        'description',
        'id'
    ]
    
    date_hierarchy = 'date'
    ordering = ['-date', '-created_at']
    
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        (_('Record Information'), {
            'fields': ('id', 'user', 'amount', 'type', 'category', 'date')
        }),
        (_('Details'), {
            'fields': ('description',)
        }),
        (_('Status'), {
            'fields': ('is_deleted',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Include deleted records in admin."""
        return super().get_queryset(request)
    
    actions = ['mark_as_deleted', 'mark_as_active']
    
    @admin.action(description='Mark selected as deleted')
    def mark_as_deleted(self, request, queryset):
        """Soft delete selected records."""
        updated = queryset.update(is_deleted=True)
        self.message_user(request, f'{updated} records marked as deleted.')
    
    @admin.action(description='Mark selected as active')
    def mark_as_active(self, request, queryset):
        """Restore soft-deleted records."""
        updated = queryset.update(is_deleted=False)
        self.message_user(request, f'{updated} records restored.')