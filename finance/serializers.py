"""
Serializers for Financial Records.
"""
from rest_framework import serializers
from decimal import Decimal
from datetime import date
from .models import FinancialRecord


class FinancialRecordSerializer(serializers.ModelSerializer):
    """
    Main serializer for Financial Records.
    """
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = FinancialRecord
        fields = [
            'id',
            'user',
            'user_email',
            'user_username',
            'amount',
            'type',
            'type_display',
            'category',
            'category_display',
            'date',
            'description',
            'is_deleted',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def validate_amount(self, value):
        """Ensure amount is positive."""
        if value <= Decimal('0'):
            raise serializers.ValidationError("Amount must be greater than zero.")
        if value > Decimal('999999999.99'):
            raise serializers.ValidationError("Amount is too large.")
        return value
    
    def validate_date(self, value):
        """Ensure date is not in the future."""
        if value > date.today():
            raise serializers.ValidationError("Date cannot be in the future.")
        return value
    
    def validate(self, data):
        transaction_type = data.get('type')
        category = data.get('category')

        income_categories = [
            FinancialRecord.Category.SALARY,
            FinancialRecord.Category.BUSINESS,
            FinancialRecord.Category.INVESTMENT,
            FinancialRecord.Category.GIFT,
        ]

        expense_categories = [
            FinancialRecord.Category.FOOD,
            FinancialRecord.Category.TRANSPORT,
            FinancialRecord.Category.UTILITIES,
            FinancialRecord.Category.ENTERTAINMENT,
            FinancialRecord.Category.HEALTHCARE,
            FinancialRecord.Category.SHOPPING,
            FinancialRecord.Category.EDUCATION,
            FinancialRecord.Category.RENT,
        ]

        if category == FinancialRecord.Category.OTHER:
            return data

        if transaction_type == FinancialRecord.TransactionType.INCOME:
            if category not in income_categories:
                raise serializers.ValidationError({
                    "category": [f"'{category}' is not a valid income category."]
                })

        elif transaction_type == FinancialRecord.TransactionType.EXPENSE:
            if category not in expense_categories:
                raise serializers.ValidationError({
                    "category": [f"'{category}' is not a valid expense category."]
                })

        return data   
    def create(self, validated_data):
        """Create record with current user."""
        # User will be set in the view
        return super().create(validated_data)


class FinancialRecordCreateSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for creating records.
    """
    
    class Meta:
        model = FinancialRecord
        fields = [
            'amount',
            'type',
            'category',
            'date',
            'description'
        ]
    
    def validate_amount(self, value):
        """Ensure amount is positive."""
        if value <= Decimal('0'):
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
    
    def validate_date(self, value):
        """Ensure date is not in the future."""
        if value > date.today():
            raise serializers.ValidationError("Date cannot be in the future.")
        return value

    def validate(self, data):
        print("VALIDATE CALLED", data)
        transaction_type = data.get('type')
        category = data.get('category')

        income_categories = [
            FinancialRecord.Category.SALARY,
            FinancialRecord.Category.BUSINESS,
            FinancialRecord.Category.INVESTMENT,
            FinancialRecord.Category.GIFT,
        ]

        expense_categories = [
            FinancialRecord.Category.FOOD,
            FinancialRecord.Category.TRANSPORT,
            FinancialRecord.Category.UTILITIES,
            FinancialRecord.Category.ENTERTAINMENT,
            FinancialRecord.Category.HEALTHCARE,
            FinancialRecord.Category.SHOPPING,
            FinancialRecord.Category.EDUCATION,
            FinancialRecord.Category.RENT,
        ]

        if category == FinancialRecord.Category.OTHER:
            return data

        if transaction_type == FinancialRecord.TransactionType.INCOME:
            if category not in income_categories:
                raise serializers.ValidationError({
                    "category": ["Invalid income category"]
                })

        elif transaction_type == FinancialRecord.TransactionType.EXPENSE:
            if category not in expense_categories:
                raise serializers.ValidationError({
                    "category": ["Invalid expense category"]
                })

        return data

class FinancialRecordListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing records.
    """
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = FinancialRecord
        fields = [
            'id',
            'amount',
            'type',
            'type_display',
            'category',
            'category_display',
            'date',
            'created_at'
        ]


class FinancialRecordUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating records.
    """
    
    class Meta:
        model = FinancialRecord
        fields = [
            'amount',
            'type',
            'category',
            'date',
            'description'
        ]
    
    def validate_amount(self, value):
        """Ensure amount is positive."""
        if value <= Decimal('0'):
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
    
    def validate_date(self, value):
        """Ensure date is not in the future."""
        if value > date.today():
            raise serializers.ValidationError("Date cannot be in the future.")
        return value