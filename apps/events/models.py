from django.db import models

from apps.accounts.models import User
from ..products.models import Product


class TasteEvent(models.Model):
    start_date = models.DateTimeField('Event starts', help_text='Format: gg/mm/yyyy hh:mm')
    end_date = models.DateTimeField('Event ends', help_text='Format: gg/mm/yyyy hh:mm')
    title = models.CharField('Title', max_length=50)
    description = models.CharField('Description', max_length=100)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Organizer')
    products = models.ManyToManyField(Product, verbose_name='Products')

    class Meta:
        ordering = ['start_date', 'title']

    def __str__(self):
        return self.title
