"""
API views for Financial Records.
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import FinancialRecord
from .serializers import (
    FinancialRecordSerializer,
    FinancialRecordCreateSerializer,
    FinancialRecordListSerializer,
    FinancialRecordUpdateSerializer
)
from .permissions import CanCreateRecord
from .filters import FinancialRecordFilter


class FinancialRecordViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Financial Records.
    
    list: GET /api/records/ - List records (filtered by role)
    create: POST /api/records/ - Create record (Admin only)
    retrieve: GET /api/records/{id}/ - Get record details
    update: PUT /api/records/{id}/ - Update record (Admin only)
    partial_update: PATCH /api/records/{id}/ - Partial update (Admin only)
    destroy: DELETE /api/records/{id}/ - Soft delete (Admin only)
    """
    permission_classes = [IsAuthenticated, CanCreateRecord]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = FinancialRecordFilter
    search_fields = ['description', 'category']
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date', '-created_at']
    
    def get_queryset(self):
        """
        Filter records based on user role:
        - Viewer: Only own records
        - Analyst: All records
        - Admin: All records
        """
        user = self.request.user
        
        # Base queryset - exclude soft-deleted records
        queryset = FinancialRecord.objects.filter(is_deleted=False)
        
        # Filter by role
        if user.role == 'VIEWER':
            # Viewers see only their own records
            queryset = queryset.filter(user=user)
        elif user.role in ['ANALYST', 'ADMIN']:
            # Analysts and Admins see all records
            pass
        
        return queryset.select_related('user')
    
    def get_serializer_class(self):
        """Use different serializers for different actions."""
        if self.action == 'list':
            return FinancialRecordListSerializer
        elif self.action == 'create':
            return FinancialRecordCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return FinancialRecordUpdateSerializer
        return FinancialRecordSerializer
    
    def perform_create(self, serializer):
        """Set the user when creating a record."""
        serializer.save(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete - mark as deleted instead of removing."""
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(
            {'message': 'Record deleted successfully'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, CanCreateRecord])
    def restore(self, request, pk=None):
        """
        POST /api/records/{id}/restore/
        Restore a soft-deleted record (Admin only).
        """
        # Get the record even if soft-deleted
        try:
            record = FinancialRecord.objects.get(pk=pk, is_deleted=True)
        except FinancialRecord.DoesNotExist:
            return Response(
                {'error': 'Record not found or not deleted'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        record.is_deleted = False
        record.save()
        
        serializer = self.get_serializer(record)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_records(self, request):
        """
        GET /api/records/my-records/
        Get current user's records only.
        """
        queryset = self.filter_queryset(
            FinancialRecord.objects.filter(user=request.user, is_deleted=False)
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def stats(self, request):
        """
        GET /api/records/stats/
        Quick statistics about records.
        """
        queryset = self.get_queryset()
        
        total_records = queryset.count()
        income_records = queryset.filter(type='INCOME').count()
        expense_records = queryset.filter(type='EXPENSE').count()
        
        from django.db.models import Sum
        total_income = queryset.filter(type='INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = queryset.filter(type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0
        
        return Response({
            'total_records': total_records,
            'income_records': income_records,
            'expense_records': expense_records,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_balance': total_income - total_expenses
        })