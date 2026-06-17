from django.db import models


class StaticPage(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField('Слаг', unique=True)
    content = models.TextField('Содержание')
    is_published = models.BooleanField('Опубликовано', default=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Статичная страница'
        verbose_name_plural = 'Статичные страницы'

    def __str__(self):
        return self.title