from django.urls import path

from .views import TableItemListAPIView

urlpatterns = [
    path('items/', TableItemListAPIView.as_view(), name='table-items'),
]
