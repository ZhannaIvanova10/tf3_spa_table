from datetime import date

from django.core.management import call_command
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import TableItem


class TableItemApiTests(APITestCase):
    def setUp(self):
        TableItem.objects.create(date=date(2024, 1, 10), name='Alpha', quantity=10, distance=100.5)
        TableItem.objects.create(date=date(2024, 2, 12), name='Beta', quantity=20, distance=250.0)
        TableItem.objects.create(date=date(2024, 3, 15), name='Gamma', quantity=5, distance=80.1)

    def test_list_returns_paginated_data(self):
        response = self.client.get(reverse('table-items'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(len(response.data['results']), 3)

    def test_sorting_by_quantity_desc(self):
        response = self.client.get(reverse('table-items'), {'ordering': '-quantity'})
        quantities = [row['quantity'] for row in response.data['results']]

        self.assertEqual(quantities, [20, 10, 5])

    def test_filter_contains_name(self):
        response = self.client.get(
            reverse('table-items'),
            {'filter_column': 'name', 'filter_condition': 'contains', 'filter_value': 'alp'},
        )

        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Alpha')

    def test_filter_gt_quantity(self):
        response = self.client.get(
            reverse('table-items'),
            {'filter_column': 'quantity', 'filter_condition': 'gt', 'filter_value': '9'},
        )

        self.assertEqual(response.data['count'], 2)

    def test_invalid_filter_value_returns_empty(self):
        response = self.client.get(
            reverse('table-items'),
            {'filter_column': 'distance', 'filter_condition': 'lt', 'filter_value': 'bad-number'},
        )

        self.assertEqual(response.data['count'], 0)


class SeedCommandTests(APITestCase):
    def test_seed_command_populates_data(self):
        self.assertEqual(TableItem.objects.count(), 0)

        call_command('seed_table_data', '--count', '10')

        self.assertEqual(TableItem.objects.count(), 10)
