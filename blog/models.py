from django.db import models

from mailings.models import NULLABLE
from users.models import User


class BlogPost(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    preview_image = models.ImageField(**NULLABLE, upload_to='blog_images/',
                                      verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')
    is_published = models.BooleanField(default=True,
                                       verbose_name='Опубликовано')
    views_count = models.PositiveIntegerField(
        default=0, verbose_name='Количество просмотров')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'записи'
