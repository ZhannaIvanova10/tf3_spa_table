from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'items', views.TableItemViewSet, basename='tableitem')

urlpatterns = [
    path('', include(router.urls)),  # Убрали 'api/' отсюда!
]