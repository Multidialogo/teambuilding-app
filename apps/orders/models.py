from django.db import models

from services.users.models import User

from ..products.models import ProductPurchaseOption


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Customer')
    priceByQuantity = models.ForeignKey(ProductPurchaseOption, on_delete=models.CASCADE, verbose_name='Price by quantity')

    class Meta:
        ordering = ['priceByQuantity']

    def __str__(self):
        return self.priceByQuantity
