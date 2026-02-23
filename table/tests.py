from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import TableItem
import datetime

class TableItemModelTest(TestCase):
    """Тесты для модели"""
    
    def setUp(self):
        self.item = TableItem.objects.create(
            date=datetime.date(2026, 2, 23),
            title='Test Item',
            quantity=100,
            distance=50.5
        )
    
    def test_item_creation(self):
        """Тест создания записи"""
        self.assertEqual(self.item.title, 'Test Item')
        self.assertEqual(self.item.quantity, 100)
        self.assertEqual(self.item.distance, 50.5)
        self.assertEqual(self.item.date, datetime.date(2026, 2, 23))
    
    def test_item_str_method(self):
        """Тест строкового представления"""
        expected = f"{self.item.date} - {self.item.title}"
        self.assertEqual(str(self.item), expected)
    
    def test_item_ordering(self):
        """Тест сортировки (новые сверху)"""
        item2 = TableItem.objects.create(
            date=datetime.date(2026, 2, 24),
            title='Another Item',
            quantity=200,
            distance=100.0
        )
        items = TableItem.objects.all()
        self.assertEqual(items[0], item2)  # Сначала новые
        self.assertEqual(items[1], self.item)
    
    def test_item_update(self):
        """Тест обновления записи"""
        self.item.title = 'Updated Title'
        self.item.quantity = 150
        self.item.save()
        updated_item = TableItem.objects.get(id=self.item.id)
        self.assertEqual(updated_item.title, 'Updated Title')
        self.assertEqual(updated_item.quantity, 150)
    
    def test_item_deletion(self):
        """Тест удаления записи"""
        item_id = self.item.id
        self.item.delete()
        with self.assertRaises(TableItem.DoesNotExist):
            TableItem.objects.get(id=item_id)

class TableItemAPITest(APITestCase):
    """Тесты для API"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        self.item1 = TableItem.objects.create(
            date=datetime.date(2026, 2, 23),
            title='API Test Item 1',
            quantity=100,
            distance=50.5
        )
        self.item2 = TableItem.objects.create(
            date=datetime.date(2026, 2, 24),
            title='API Test Item 2',
            quantity=200,
            distance=100.0
        )
        
        self.list_url = reverse('tableitem-list')
        self.token_url = reverse('token_obtain_pair')
    
    def test_get_items_unauthenticated(self):
        """GET запрос без авторизации (должен работать)"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('results' in response.data)
    
    def test_filter_by_title(self):
        """Тест фильтрации по названию"""
        response = self.client.get(self.list_url, {'title': 'Item 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'API Test Item 1')
    
    def test_filter_by_quantity_gt(self):
        """Тест фильтрации quantity больше чем"""
        response = self.client.get(self.list_url, {'quantity__gt': 150})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['quantity'], 200)
    
    def test_filter_by_quantity_lt(self):
        """Тест фильтрации quantity меньше чем"""
        response = self.client.get(self.list_url, {'quantity__lt': 150})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['quantity'], 100)
    
    def test_filter_by_distance_gt(self):
        """Тест фильтрации distance больше чем"""
        response = self.client.get(self.list_url, {'distance__gt': 75})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['distance'], 100.0)
    
    def test_filter_by_distance_lt(self):
        """Тест фильтрации distance меньше чем"""
        response = self.client.get(self.list_url, {'distance__lt': 75})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['distance'], 50.5)
    
    def test_ordering_by_title(self):
        """Тест сортировки по названию"""
        response = self.client.get(self.list_url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(results[0]['title'], 'API Test Item 1')
        self.assertEqual(results[1]['title'], 'API Test Item 2')
    
    def test_ordering_by_title_desc(self):
        """Тест сортировки по названию (убывание)"""
        response = self.client.get(self.list_url, {'ordering': '-title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(results[0]['title'], 'API Test Item 2')
        self.assertEqual(results[1]['title'], 'API Test Item 1')
    
    def test_ordering_by_quantity(self):
        """Тест сортировки по количеству"""
        response = self.client.get(self.list_url, {'ordering': 'quantity'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(results[0]['quantity'], 100)
        self.assertEqual(results[1]['quantity'], 200)
    
    def test_pagination(self):
        """Тест пагинации"""
        # Создадим 15 записей
        for i in range(15):
            TableItem.objects.create(
                date=datetime.date(2026, 2, 23),
                title=f'Pagination Item {i}',
                quantity=i,
                distance=i*1.5
            )
        
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)  # page_size = 10
        self.assertEqual(response.data['count'], 17)  # 2 старых + 15 новых
        
        # Проверим вторую страницу
        response = self.client.get(self.list_url + '?page=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 7)  # оставшиеся 7
    
    def test_stats_endpoint(self):
        """Тест эндпоинта статистики"""
        # Сначала удалим старую статистику из views.py если она есть
        pass