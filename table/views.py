from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
import csv
from .models import TableItem
from .serializers import TableItemSerializer

class TableItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet для CRUD операций с таблицей
    Поддерживает фильтрацию, поиск и сортировку
    """
    queryset = TableItem.objects.all()
    serializer_class = TableItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title', 'status']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Статистика по статусам"""
        total = self.queryset.count()
        new = self.queryset.filter(status='new').count()
        in_progress = self.queryset.filter(status='in_progress').count()
        completed = self.queryset.filter(status='completed').count()
        cancelled = self.queryset.filter(status='cancelled').count()
        
        return Response({
            'total': total,
            'new': new,
            'in_progress': in_progress,
            'completed': completed,
            'cancelled': cancelled,
        })
    
    @action(detail=False, methods=['post'])
    def bulk_delete(self, request):
        """Массовое удаление записей"""
        ids = request.data.get('ids', [])
        deleted, _ = self.queryset.filter(id__in=ids).delete()
        return Response({'deleted': deleted}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        """Экспорт данных в CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="table_items.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Title', 'Description', 'Status', 'Created At', 'Updated At'])
        
        for item in self.queryset:
            writer.writerow([
                item.id,
                item.title,
                item.description,
                item.status,
                item.created_at,
                item.updated_at
            ])
        
        return response