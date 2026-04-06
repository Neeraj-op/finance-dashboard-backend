"""
Django filters for Financial Records.
"""
import django_filters
from .models import FinancialRecord


class FinancialRecordFilter(django_filters.FilterSet):
    """
    Filter class for Financial Records.
    Enables filtering by type, category, date range, and amount range.
    """
    # Date range filters
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    
    # Amount range filters
    amount_min = django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    amount_max = django_filters.NumberFilter(field_name='amount', lookup_expr='lte')
    
    # Exact filters
    type = django_filters.ChoiceFilter(choices=FinancialRecord.TransactionType.choices)
    category = django_filters.ChoiceFilter(choices=FinancialRecord.Category.choices)
    
    # Year and month filters
    year = django_filters.NumberFilter(field_name='date', lookup_expr='year')
    month = django_filters.NumberFilter(field_name='date', lookup_expr='month')
    
    class Meta:
        model = FinancialRecord
        fields = ['type', 'category', 'date_from', 'date_to', 'amount_min', 'amount_max', 'year', 'month']