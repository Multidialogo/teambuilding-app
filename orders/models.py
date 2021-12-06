from django.db import models

from products.models import PriceByQuantity
from users.models import User


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Customer')
    priceByQuantity = models.ForeignKey(PriceByQuantity, on_delete=models.CASCADE, verbose_name='Price by quantity')

    class Meta:
        ordering = ['priceByQuantity']

    def __str__(self):
        return self.priceByQuantity
