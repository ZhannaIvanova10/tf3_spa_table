from rest_framework import serializers

from .models import TableItem


class TableItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableItem
        fields = ['id', 'date', 'name', 'quantity', 'distance']
        read_only_fields = ['id']
