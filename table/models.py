from django.db import models


class TableItem(models.Model):
    """Модель для элементов таблицы"""
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    status = models.CharField('Статус', max_length=50,
                              choices=[
                                  ('new', 'Новый'),
                                  ('in_progress', 'В работе'),
                                  ('completed', 'Завершен'),
                                  ('cancelled', 'Отменен')
                              ],
                              default='new')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Элемент таблицы'
        verbose_name_plural = 'Элементы таблицы'
        ordering = ['-created_at']

    def __str__(self):
        return self.title