from django.db import models
from django.urls import reverse, NoReverseMatch


class Menu(models.Model):
    title = models.CharField(
        verbose_name='Название меню',
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    menu = models.ForeignKey(
        Menu,
        verbose_name='Связь с меню',
        on_delete=models.CASCADE,
        related_name='items',
    )
    parent = models.ForeignKey(
        'self',
        verbose_name='Родительский пункт меню',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children',
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=100,
    )
    url = models.CharField(
        verbose_name='Явный URL',
        max_length=200,
        blank=True,
    )
    named_url = models.CharField(
        verbose_name='Именованный URL',
        max_length=200,
        blank=True,
    )
    order = models.PositiveIntegerField(
        verbose_name='Порядок вывода',
        default=0,
    )

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        ordering = ['order']

    def get_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return '#'
        return self.url or '#'

    def __str__(self):
        return self.title
