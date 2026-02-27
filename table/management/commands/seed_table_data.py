import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand

from table.models import TableItem


class Command(BaseCommand):
    help = 'Заполняет таблицу случайными данными для демонстрации.'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=100)
        parser.add_argument('--force', action='store_true')

    def handle(self, *args, **options):
        count = options['count']
        force = options['force']

        if TableItem.objects.exists() and not force:
            self.stdout.write(self.style.WARNING('Таблица уже содержит данные, пропуск заполнения.'))
            return

        if force:
            TableItem.objects.all().delete()

        base_date = date.today()
        names = ['Маршрут A', 'Маршрут B', 'Маршрут C', 'Тестовый путь', 'Городская линия']

        records = []
        for _ in range(count):
            records.append(
                TableItem(
                    date=base_date - timedelta(days=random.randint(0, 365)),
                    name=f"{random.choice(names)} #{random.randint(1, 999)}",
                    quantity=random.randint(1, 500),
                    distance=round(random.uniform(0.5, 2500.0), 2),
                )
            )

        TableItem.objects.bulk_create(records)
        self.stdout.write(self.style.SUCCESS(f'Создано записей: {len(records)}'))
