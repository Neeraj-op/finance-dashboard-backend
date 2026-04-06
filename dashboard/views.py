"""
API views for Dashboard Analytics.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta

from .services import DashboardService
from .serializers import (
    DashboardSummarySerializer,
    CategoryWiseSerializer,
    TrendDataSerializer,
    RecentActivitySerializer,
    DateRangeFilterSerializer
)


class DashboardViewSet(viewsets.ViewSet):
    """
    API endpoints for dashboard analytics.
    
    All endpoints require authentication.
    Data is filtered based on user role.
    """
    permission_classes = [IsAuthenticated]
    
    def _get_date_range(self, request):
        """Extract and validate date range from request."""
        serializer = DateRangeFilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        return (
            serializer.validated_data.get('date_from'),
            serializer.validated_data.get('date_to')
        )
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        GET /api/dashboard/summary/
        
        Get overall summary statistics.
        
        Query params:
            - date_from (optional): Start date (YYYY-MM-DD)
            - date_to (optional): End date (YYYY-MM-DD)
        
        Returns:
            - total_income
            - total_expenses
            - net_balance
            - record_count
            - income_count
            - expense_count
        """
        date_from, date_to = self._get_date_range(request)
        
        service = DashboardService(request.user, date_from, date_to)
        summary_data = service.get_summary()
        
        serializer = DashboardSummarySerializer(data=summary_data)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.validated_data)
    
    @action(detail=False, methods=['get'], url_path='category-wise')
    def category_wise(self, request):
        """
        GET /api/dashboard/category-wise/
        
        Get category-wise breakdown of income and expenses.
        
        Query params:
            - date_from (optional): Start date
            - date_to (optional): End date
        
        Returns:
            - income_by_category: List of categories with totals and percentages
            - expense_by_category: List of categories with totals and percentages
            - total_income
            - total_expenses
        """
        date_from, date_to = self._get_date_range(request)
        
        service = DashboardService(request.user, date_from, date_to)
        category_data = service.get_category_wise_breakdown()
        
        serializer = CategoryWiseSerializer(data=category_data)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.validated_data)
    
    @action(detail=False, methods=['get'])
    def trends(self, request):
        """
        GET /api/dashboard/trends/
        
        Get trends data (monthly or weekly).
        
        Query params:
            - period: 'monthly' or 'weekly' (default: monthly)
            - date_from (optional): Start date
            - date_to (optional): End date
        
        Returns:
            List of periods with income, expenses, net, and count
        """
        date_from, date_to = self._get_date_range(request)
        period = request.query_params.get('period', 'monthly')
        
        service = DashboardService(request.user, date_from, date_to)
        
        if period == 'weekly':
            trends_data = service.get_weekly_trends()
        else:
            trends_data = service.get_monthly_trends()
        
        serializer = TrendDataSerializer(data=trends_data, many=True)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.validated_data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        GET /api/dashboard/recent/
        
        Get recent transactions.
        
        Query params:
            - limit: Number of records (default: 10, max: 50)
        
        Returns:
            List of recent transactions
        """
        try:
            limit = int(request.query_params.get('limit', 10))
            limit = min(limit, 50)  # Cap at 50
        except ValueError:
            limit = 10
        
        service = DashboardService(request.user)
        recent_records = service.get_recent_activity(limit)
        
        # Format data for serializer
        recent_data = []
        for record in recent_records:
            recent_data.append({
                'id': record.id,
                'amount': record.amount,
                'type': record.type,
                'type_display': record.get_type_display(),
                'category': record.category,
                'category_display': record.get_category_display(),
                'date': record.date,
                'description': record.description,
                'created_at': record.created_at
            })
        
        serializer = RecentActivitySerializer(data=recent_data, many=True)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.validated_data)
    
    @action(detail=False, methods=['get'], url_path='top-expenses')
    def top_expenses(self, request):
        """
        GET /api/dashboard/top-expenses/
        
        Get top expense categories.
        
        Query params:
            - limit: Number of categories (default: 5)
            - date_from (optional): Start date
            - date_to (optional): End date
        
        Returns:
            List of top expense categories with totals
        """
        date_from, date_to = self._get_date_range(request)
        
        try:
            limit = int(request.query_params.get('limit', 5))
        except ValueError:
            limit = 5
        
        service = DashboardService(request.user, date_from, date_to)
        top_expenses = service.get_top_expenses(limit)
        
        return Response(top_expenses)
    
    @action(detail=False, methods=['get'])
    def comparison(self, request):
        """
        GET /api/dashboard/comparison/
        
        Compare current period with previous period.
        
        Query params:
            - period: 'month' or 'year' (default: month)
        
        Returns:
            Comparison data with growth percentages
        """
        period_type = request.query_params.get('period', 'month')
        
        today = datetime.now().date()
        
        if period_type == 'year':
            # Current year vs previous year
            current_start = datetime(today.year, 1, 1).date()
            current_end = today
            previous_start = datetime(today.year - 1, 1, 1).date()
            previous_end = datetime(today.year - 1, 12, 31).date()
        else:
            # Current month vs previous month
            current_start = datetime(today.year, today.month, 1).date()
            current_end = today
            
            # Calculate previous month
            if today.month == 1:
                previous_year = today.year - 1
                previous_month = 12
            else:
                previous_year = today.year
                previous_month = today.month - 1
            
            previous_start = datetime(previous_year, previous_month, 1).date()
            
            # Last day of previous month
            if previous_month == 12:
                previous_end = datetime(previous_year, 12, 31).date()
            else:
                previous_end = (datetime(previous_year, previous_month + 1, 1) - timedelta(days=1)).date()
        
        service = DashboardService(request.user)
        comparison_data = service.get_comparison_data(
            current_start, current_end,
            previous_start, previous_end
        )
        
        return Response(comparison_data)