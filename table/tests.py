from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import TableItem

class TableItemModelTest(TestCase):
    """Тесты для модели"""
    
    def setUp(self):
        self.item = TableItem.objects.create(
            title='Test Item',
            description='Test Description',
            status='new'
        )
    
    def test_item_creation(self):
        """Тест создания записи"""
        self.assertEqual(self.item.title, 'Test Item')
        self.assertEqual(self.item.status, 'new')
        self.assertIsNotNone(self.item.created_at)
    
    def test_item_str_method(self):
        """Тест строкового представления"""
        self.assertEqual(str(self.item), 'Test Item')
    
    def test_item_ordering(self):
        """Тест сортировки (новые сверху)"""
        item2 = TableItem.objects.create(
            title='Another Item',
            status='in_progress'
        )
        items = TableItem.objects.all()
        self.assertEqual(items[0], item2)  # Сначала новые
        self.assertEqual(items[1], self.item)
    
    def test_item_update(self):
        """Тест обновления записи"""
        self.item.title = 'Updated Title'
        self.item.save()
        updated_item = TableItem.objects.get(id=self.item.id)
        self.assertEqual(updated_item.title, 'Updated Title')
    
    def test_item_deletion(self):
        """Тест удаления записи"""
        item_id = self.item.id
        self.item.delete()
        with self.assertRaises(TableItem.DoesNotExist):
            TableItem.objects.get(id=item_id)

class TableItemAPITest(APITestCase):
    """Тесты для API"""
    
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Создаем тестовые записи
        self.item1 = TableItem.objects.create(
            title='API Test Item 1',
            description='Description 1',
            status='new'
        )
        self.item2 = TableItem.objects.create(
            title='API Test Item 2',
            description='Description 2',
            status='in_progress'
        )
        
        self.list_url = reverse('tableitem-list')
        self.token_url = reverse('token_obtain_pair')
    
    def test_get_items_unauthenticated(self):
        """GET запрос без авторизации (должен работать)"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_create_item_unauthenticated(self):
        """POST запрос без авторизации (должен быть запрещен)"""
        data = {'title': 'New Item', 'status': 'new'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_item_authenticated(self):
        """POST запрос с авторизацией"""
        # Получаем токен
        response = self.client.post(self.token_url, {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']
        
        # Создаем запись с токеном
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'title': 'Auth Item', 'description': 'Test', 'status': 'in_progress'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Auth Item')
    
    def test_filter_by_status(self):
        """Тест фильтрации по статусу"""
        response = self.client.get(self.list_url, {'status': 'new'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'new')
    
    def test_search_by_title(self):
        """Тест поиска по названию"""
        response = self.client.get(self.list_url, {'search': 'Item 1'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'API Test Item 1')
    
    def test_search_by_description(self):
        """Тест поиска по описанию"""
        response = self.client.get(self.list_url, {'search': 'Description 2'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['description'], 'Description 2')
    
    def test_ordering_by_title(self):
        """Тест сортировки по названию"""
        response = self.client.get(self.list_url, {'ordering': 'title'})
        self.assertEqual(response.data[0]['title'], 'API Test Item 1')
        self.assertEqual(response.data[1]['title'], 'API Test Item 2')
    
    def test_retrieve_single_item(self):
        """Тест получения одной записи"""
        url = reverse('tableitem-detail', args=[self.item1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'API Test Item 1')
    
    def test_update_item_authenticated(self):
        """Тест обновления записи"""
        # Получаем токен
        response = self.client.post(self.token_url, {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        token = response.data['access']
        
        # Обновляем запись
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('tableitem-detail', args=[self.item1.id])
        data = {'title': 'Updated Title', 'status': 'completed'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')
        self.assertEqual(response.data['status'], 'completed')
    
    def test_delete_item_authenticated(self):
        """Тест удаления записи"""
        # Получаем токен
        response = self.client.post(self.token_url, {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        token = response.data['access']
        
        # Удаляем запись
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('tableitem-detail', args=[self.item1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Проверяем, что запись удалена
        response = self.client.get(self.list_url)
        self.assertEqual(len(response.data), 1)
    
    def test_stats_endpoint(self):
        """Тест эндпоинта статистики"""
        url = reverse('tableitem-stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total'], 2)
        self.assertEqual(response.data['new'], 1)
        self.assertEqual(response.data['in_progress'], 1)
    
    def test_bulk_delete_authenticated(self):
        """Тест массового удаления"""
        # Получаем токен
        response = self.client.post(self.token_url, {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        token = response.data['access']
        
        # Массовое удаление
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('tableitem-bulk-delete')
        data = {'ids': [self.item1.id, self.item2.id]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Проверяем, что все записи удалены
        response = self.client.get(self.list_url)
        self.assertEqual(len(response.data), 0)