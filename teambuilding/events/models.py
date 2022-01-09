from django.core.exceptions import ValidationError
from django.db import models

from teambuilding.users.models import User
from teambuilding.products.models import Product


class TasteEvent(models.Model):
    start_date = models.DateTimeField('inizio evento', help_text='Format: gg/mm/yyyy hh:mm')
    end_date = models.DateTimeField('fine evento', help_text='Format: gg/mm/yyyy hh:mm')
    title = models.CharField('titolo', max_length=50)
    description = models.CharField('descrizione', max_length=100)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='organizzatore')
    products = models.ManyToManyField(Product, verbose_name='prodotti')

    class Meta:
        ordering = ['start_date', 'title']
        verbose_name = 'evento degustazione'
        verbose_name_plural = 'eventi degustazione'

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.start_date > self.end_date:
            raise ValidationError({
                'start_date': 'La data di fine evento deve essere successiva a quella di inizio evento.',
                'end_date': 'La data di fine evento deve essere successiva a quella di inizio evento.'
            })
