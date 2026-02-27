from django.contrib import admin

from .models import TableItem


@admin.register(TableItem)
class TableItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'name', 'quantity', 'distance')
    search_fields = ('name',)
    list_filter = ('date',)
