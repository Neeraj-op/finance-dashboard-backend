"""
Financial Record model for storing transactions.
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class FinancialRecord(models.Model):
    """
    Model for storing financial transactions (income/expenses).
    """
    
    class TransactionType(models.TextChoices):
        INCOME = 'INCOME', _('Income')
        EXPENSE = 'EXPENSE', _('Expense')
    
    class Category(models.TextChoices):
        # Income categories
        SALARY = 'SALARY', _('Salary')
        BUSINESS = 'BUSINESS', _('Business')
        INVESTMENT = 'INVESTMENT', _('Investment')
        GIFT = 'GIFT', _('Gift')
        
        # Expense categories
        FOOD = 'FOOD', _('Food & Dining')
        TRANSPORT = 'TRANSPORT', _('Transportation')
        UTILITIES = 'UTILITIES', _('Utilities')
        ENTERTAINMENT = 'ENTERTAINMENT', _('Entertainment')
        HEALTHCARE = 'HEALTHCARE', _('Healthcare')
        SHOPPING = 'SHOPPING', _('Shopping')
        EDUCATION = 'EDUCATION', _('Education')
        RENT = 'RENT', _('Rent')
        
        # General
        OTHER = 'OTHER', _('Other')
    
    # Primary key as UUID for better security
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Foreign key to User
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='financial_records',
        help_text=_('User who owns this record')
    )
    
    # Amount (positive decimal, validation in serializer)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text=_('Transaction amount')
    )
    
    # Transaction type
    type = models.CharField(
        max_length=10,
        choices=TransactionType.choices,
        help_text=_('Income or Expense')
    )
    
    # Category
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        help_text=_('Transaction category')
    )
    
    # Date of transaction
    date = models.DateField(
        help_text=_('Date when transaction occurred')
    )
    
    # Description/Notes
    description = models.TextField(
        blank=True,
        help_text=_('Additional notes about this transaction')
    )
    
    # Soft delete flag
    is_deleted = models.BooleanField(
        default=False,
        help_text=_('Soft delete - record is hidden but not removed')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'financial_records'
        ordering = ['-date', '-created_at']
        verbose_name = _('Financial Record')
        verbose_name_plural = _('Financial Records')
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['type', 'category']),
            models.Index(fields=['date']),
            models.Index(fields=['is_deleted']),
        ]
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.amount} ({self.date})"
    
    def save(self, *args, **kwargs):
        """Override save to add custom logic."""
        # You can add validation or business logic here
        super().save(*args, **kwargs)
    
    @property
    def is_income(self):
        """Check if this is an income record."""
        return self.type == self.TransactionType.INCOME
    
    @property
    def is_expense(self):
        """Check if this is an expense record."""
        return self.type == self.TransactionType.EXPENSE
    
    @classmethod
    def get_active_records(cls):
        """Get all non-deleted records."""
        return cls.objects.filter(is_deleted=False)
    
    @classmethod
    def get_user_records(cls, user):
        """Get all active records for a specific user."""
        return cls.get_active_records().filter(user=user)