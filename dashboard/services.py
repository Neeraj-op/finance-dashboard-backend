"""
Business logic for dashboard analytics.
Separated from views for better organization and testability.
"""
from django.db.models import Sum, Count, Q, F
from django.db.models.functions import TruncMonth, TruncWeek
from decimal import Decimal
from datetime import datetime, timedelta

from finance.models import FinancialRecord


class DashboardService:
    """Service class for dashboard analytics."""
    
    def __init__(self, user, date_from=None, date_to=None):
        """
        Initialize service with user and optional date range.
        
        Args:
            user: User object
            date_from: Start date for filtering (optional)
            date_to: End date for filtering (optional)
        """
        self.user = user
        self.date_from = date_from
        self.date_to = date_to
    
    def get_base_queryset(self):
        """Get base queryset filtered by user role and date range."""
        # Start with active records only
        queryset = FinancialRecord.objects.filter(is_deleted=False)
        
        # Filter by user role
        if self.user.role == 'VIEWER':
            queryset = queryset.filter(user=self.user)
        # Analysts and Admins see all records
        
        # Filter by date range
        if self.date_from:
            queryset = queryset.filter(date__gte=self.date_from)
        if self.date_to:
            queryset = queryset.filter(date__lte=self.date_to)
        
        return queryset
    
    def get_summary(self):
        """
        Calculate overall summary statistics.
        
        Returns:
            dict: Summary with income, expenses, balance, counts
        """
        queryset = self.get_base_queryset()
        
        # Aggregate by type
        income_data = queryset.filter(type='INCOME').aggregate(
            total=Sum('amount'),
            count=Count('id')
        )
        
        expense_data = queryset.filter(type='EXPENSE').aggregate(
            total=Sum('amount'),
            count=Count('id')
        )
        
        total_income = income_data['total'] or Decimal('0.00')
        total_expenses = expense_data['total'] or Decimal('0.00')
        
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_balance': total_income - total_expenses,
            'record_count': queryset.count(),
            'income_count': income_data['count'],
            'expense_count': expense_data['count'],
            'period_start': self.date_from,
            'period_end': self.date_to
        }
    

    def get_category_wise_breakdown(self):
        queryset = self.get_base_queryset()

        from decimal import Decimal, ROUND_HALF_UP
        from django.db.models import Sum, Count
        # Income by category
        income_by_category = list(
            queryset.filter(type='INCOME')
            .values('category')
            .annotate(
                total_amount=Sum('amount'),
                count=Count('id')
            )
            .order_by('-total_amount')
        )

        # Expense by category
        expense_by_category = list(
            queryset.filter(type='EXPENSE')
            .values('category')
            .annotate(
                total_amount=Sum('amount'),
                count=Count('id')
            )
            .order_by('-total_amount')
        )

        # Totals
        total_income = sum((item['total_amount'] for item in income_by_category), Decimal('0.00'))
        total_expenses = sum((item['total_amount'] for item in expense_by_category), Decimal('0.00'))

        # Category choices mapping
        category_map = dict(FinancialRecord.Category.choices)

        # income processing
        income_list = []
        for item in income_by_category:
            category = item['category']

            percentage = (
                (item['total_amount'] / total_income * Decimal('100'))
                if total_income > 0 else Decimal('0.00')
            ).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            income_list.append({
                "category": str(category),
                "category_display": str(category_map.get(category, category)),
                "total_amount": item['total_amount'],
                "count": item['count'],
                "percentage": percentage
            })

        # expense processing
        expense_list = []
        for item in expense_by_category:
            category = item['category']

            percentage = (
                (item['total_amount'] / total_expenses * Decimal('100'))
                if total_expenses > 0 else Decimal('0.00')
            ).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            expense_list.append({
                "category": str(category),
                "category_display": str(category_map.get(category, category)),
                "total_amount": item['total_amount'],
                "count": item['count'],
                "percentage": percentage
            })

        return {
            "income_by_category": income_list,
            "expense_by_category": expense_list,
            "total_income": total_income,
            "total_expenses": total_expenses
        }

    def get_monthly_trends(self):
        """
        Get monthly trends for income and expenses.
        
        Returns:
            list: Monthly data with income, expenses, net
        """
        queryset = self.get_base_queryset()
        
        # Group by month
        monthly_data = queryset.annotate(
            month=TruncMonth('date')
        ).values('month').annotate(
            income=Sum('amount', filter=Q(type='INCOME')),
            expenses=Sum('amount', filter=Q(type='EXPENSE')),
            count=Count('id')
        ).order_by('month')
        
        # Format results
        trends = []
        for item in monthly_data:
            income = item['income'] or Decimal('0.00')
            expenses = item['expenses'] or Decimal('0.00')
            
            trends.append({
                'period': item['month'].strftime('%Y-%m'),
                'income': income,
                'expenses': expenses,
                'net': income - expenses,
                'count': item['count']
            })
        
        return trends
    
    def get_weekly_trends(self):
        """
        Get weekly trends for income and expenses.
        
        Returns:
            list: Weekly data with income, expenses, net
        """
        queryset = self.get_base_queryset()
        
        # Group by week
        weekly_data = queryset.annotate(
            week=TruncWeek('date')
        ).values('week').annotate(
            income=Sum('amount', filter=Q(type='INCOME')),
            expenses=Sum('amount', filter=Q(type='EXPENSE')),
            count=Count('id')
        ).order_by('week')
        
        # Format results
        trends = []
        for item in weekly_data:
            income = item['income'] or Decimal('0.00')
            expenses = item['expenses'] or Decimal('0.00')
            
            # Format week as YYYY-Wxx
            week_num = item['week'].isocalendar()[1]
            year = item['week'].year
            
            trends.append({
                'period': f"{year}-W{week_num:02d}",
                'income': income,
                'expenses': expenses,
                'net': income - expenses,
                'count': item['count']
            })
        
        return trends
    
    def get_recent_activity(self, limit=10):
        """
        Get recent transactions.
        
        Args:
            limit: Number of recent records to return
            
        Returns:
            queryset: Recent records
        """
        queryset = self.get_base_queryset()
        return queryset.order_by('-date', '-created_at')[:limit]
    
    def get_top_expenses(self, limit=5):
        """
        Get top expense categories.
        
        Args:
            limit: Number of top categories to return
            
        Returns:
            list: Top expense categories with totals
        """
        queryset = self.get_base_queryset().filter(type='EXPENSE')
        
        top_expenses = queryset.values('category').annotate(
            total_amount=Sum('amount'),
            count=Count('id')
        ).order_by('-total_amount')[:limit]
        
        result = []
        for item in top_expenses:
            item['category_display'] = dict(FinancialRecord.Category.choices).get(
                item['category'], item['category']
            )
            result.append(item)
        
        return result
    
    def get_comparison_data(self, current_start, current_end, previous_start, previous_end):
        """
        Compare two time periods.
        
        Args:
            current_start: Start date of current period
            current_end: End date of current period
            previous_start: Start date of previous period
            previous_end: End date of previous period
            
        Returns:
            dict: Comparison data with growth percentages
        """
        # Current period
        current_service = DashboardService(self.user, current_start, current_end)
        current_summary = current_service.get_summary()
        
        # Previous period
        previous_service = DashboardService(self.user, previous_start, previous_end)
        previous_summary = previous_service.get_summary()
        
        # Calculate growth
        def calculate_growth(current, previous):
            if previous == 0:
                return Decimal('100.00') if current > 0 else Decimal('0.00')
            return ((current - previous) / previous * 100)
        
        return {
            'current': current_summary,
            'previous': previous_summary,
            'growth': {
                'income': calculate_growth(
                    current_summary['total_income'],
                    previous_summary['total_income']
                ),
                'expenses': calculate_growth(
                    current_summary['total_expenses'],
                    previous_summary['total_expenses']
                ),
                'net_balance': calculate_growth(
                    current_summary['net_balance'],
                    previous_summary['net_balance']
                ),
            }
        }