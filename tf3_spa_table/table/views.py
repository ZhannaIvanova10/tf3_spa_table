from datetime import date

from django.db.models import QuerySet
from django.utils.dateparse import parse_date
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from .models import TableItem
from .serializers import TableItemSerializer


class TableItemPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class TableItemListAPIView(generics.ListAPIView):
    serializer_class = TableItemSerializer
    pagination_class = TableItemPagination

    def get_queryset(self) -> QuerySet[TableItem]:
        queryset = TableItem.objects.all()
        queryset = self._apply_filter(queryset)
        queryset = self._apply_sorting(queryset)
        return queryset

    def _apply_sorting(self, queryset: QuerySet[TableItem]) -> QuerySet[TableItem]:
        ordering = self.request.query_params.get('ordering', '')
        allowed_ordering = {'name', 'quantity', 'distance'}

        field = ordering[1:] if ordering.startswith('-') else ordering
        if field in allowed_ordering:
            return queryset.order_by(ordering)
        return queryset.order_by('-date')

    def _apply_filter(self, queryset: QuerySet[TableItem]) -> QuerySet[TableItem]:
        column = self.request.query_params.get('filter_column', '')
        condition = self.request.query_params.get('filter_condition', '')
        raw_value = self.request.query_params.get('filter_value', '').strip()

        if not column or not condition or raw_value == '':
            return queryset

        if column not in {'date', 'name', 'quantity', 'distance'}:
            return queryset

        lookup = self._build_lookup(column, condition)
        if not lookup:
            return queryset

        parsed_value = self._parse_value(column, raw_value)
        if parsed_value is None:
            return queryset.none()

        return queryset.filter(**{lookup: parsed_value})

    @staticmethod
    def _build_lookup(column: str, condition: str) -> str:
        mapping = {
            'eq': '',
            'contains': '__icontains',
            'gt': '__gt',
            'lt': '__lt',
        }
        suffix = mapping.get(condition)
        if suffix is None:
            return ''
        return f'{column}{suffix}'

    @staticmethod
    def _parse_value(column: str, raw_value: str):
        if column == 'date':
            parsed = parse_date(raw_value)
            return parsed if isinstance(parsed, date) else None
        if column == 'quantity':
            return int(raw_value) if raw_value.isdigit() else None
        if column == 'distance':
            try:
                return float(raw_value)
            except ValueError:
                return None
        return raw_value
