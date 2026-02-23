from django.db import models

class TableItem(models.Model):
    date = models.DateField('Дата')
    title = models.CharField('Название', max_length=200)
    quantity = models.IntegerField('Количество')
    distance = models.FloatField('Расстояние')
    
    class Meta:
        verbose_name = 'Элемент таблицы'
        verbose_name_plural = 'Элементы таблицы'
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.date} - {self.title}"