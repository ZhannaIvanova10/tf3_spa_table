import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from table.models import TableItem

class Command(BaseCommand):
    help = 'Заполняет базу данных случайными значениями'
    
    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=100, help='Количество записей')
    
    def handle(self, *args, **kwargs):
        count = kwargs['count']
        
        # Очистим существующие данные
        TableItem.objects.all().delete()
        
        # Создадим новые записи
        start_date = date(2026, 1, 1)
        for i in range(count):
            random_days = random.randint(0, 365)
            TableItem.objects.create(
                date=start_date + timedelta(days=random_days),
                title=f'Item {i+1}',
                quantity=random.randint(1, 1000),
                distance=round(random.uniform(1.0, 1000.0), 2)
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Успешно создано {count} записей')
        )
