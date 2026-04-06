"""
Serializers for Dashboard Analytics.
"""
from rest_framework import serializers
from decimal import Decimal


class DashboardSummarySerializer(serializers.Serializer):
    """
    Serializer for dashboard summary data.
    """
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    net_balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    record_count = serializers.IntegerField()
    income_count = serializers.IntegerField()
    expense_count = serializers.IntegerField()
    period_start = serializers.DateField(required=False, allow_null=True)
    period_end = serializers.DateField(required=False, allow_null=True)


class CategorySummarySerializer(serializers.Serializer):
    """
    Serializer for category-wise summary.
    """
    category = serializers.CharField()
    category_display = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    count = serializers.IntegerField()
    percentage = serializers.DecimalField(max_digits=6, decimal_places=2, required=False)


class CategoryWiseSerializer(serializers.Serializer):
    """
    Serializer for category-wise breakdown.
    """
    income_by_category = CategorySummarySerializer(many=True)
    expense_by_category = CategorySummarySerializer(many=True)
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)


class TrendDataSerializer(serializers.Serializer):
    """
    Serializer for trend data (monthly/weekly).
    """
    period = serializers.CharField()  # e.g., "2024-01" or "2024-W01"
    income = serializers.DecimalField(max_digits=12, decimal_places=2)
    expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    net = serializers.DecimalField(max_digits=12, decimal_places=2)
    count = serializers.IntegerField()


class RecentActivitySerializer(serializers.Serializer):
    """
    Serializer for recent transactions.
    """
    id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    type = serializers.CharField()
    type_display = serializers.CharField()
    category = serializers.CharField()
    category_display = serializers.CharField()
    date = serializers.DateField()
    description = serializers.CharField()
    created_at = serializers.DateTimeField()


class DateRangeFilterSerializer(serializers.Serializer):
    """
    Serializer for validating date range filters.
    """
    date_from = serializers.DateField(required=False, allow_null=True)
    date_to = serializers.DateField(required=False, allow_null=True)
    
    def validate(self, attrs):
        """Ensure date_from is before date_to."""
        date_from = attrs.get('date_from')
        date_to = attrs.get('date_to')
        
        if date_from and date_to:
            if date_from > date_to:
                raise serializers.ValidationError({
                    'date_from': 'Start date must be before end date.'
                })
        
        return attrs