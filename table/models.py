from django.db import models


class TableItem(models.Model):
    date = models.DateField('Дата')
    name = models.CharField('Название', max_length=255)
    quantity = models.PositiveIntegerField('Количество')
    distance = models.FloatField('Расстояние')

    class Meta:
        verbose_name = 'Элемент таблицы'
        verbose_name_plural = 'Элементы таблицы'
        ordering = ['-date']

    def __str__(self) -> str:
        return f'{self.name} ({self.date})'
