from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import TableItem
from .serializers import TableItemSerializer

class TableItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet для CRUD операций с таблицей
    """
    queryset = TableItem.objects.all()
    serializer_class = TableItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title', 'status']
    ordering = ['-created_at']