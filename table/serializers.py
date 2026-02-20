from rest_framework import serializers
from .models import TableItem

class TableItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableItem
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']