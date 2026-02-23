from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import TableItem
from .serializers import TableItemSerializer
import django_filters

# Кастомный фильтр с условиями
class TableItemFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    quantity = django_filters.NumberFilter()
    quantity__gt = django_filters.NumberFilter(field_name='quantity', lookup_expr='gt')
    quantity__lt = django_filters.NumberFilter(field_name='quantity', lookup_expr='lt')
    distance = django_filters.NumberFilter()
    distance__gt = django_filters.NumberFilter(field_name='distance', lookup_expr='gt')
    distance__lt = django_filters.NumberFilter(field_name='distance', lookup_expr='lt')
    
    class Meta:
        model = TableItem
        fields = ['title', 'quantity', 'distance']

# Пагинация
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class TableItemViewSet(viewsets.ModelViewSet):
    queryset = TableItem.objects.all()
    serializer_class = TableItemSerializer
    filterset_class = TableItemFilter
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  # Изменено здесь!
    ordering_fields = ['title', 'quantity', 'distance']
    ordering = ['-date']
    pagination_class = StandardResultsSetPagination