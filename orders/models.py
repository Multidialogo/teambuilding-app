from django.db import models

from events.models import PriceByQuantity
from users.models import User

# Create your models here.
class Order(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='Customer')
    priceByQuantity = models.ForeignKey(PriceByQuantity,on_delete=models.CASCADE, verbose_name='Price by quantity')

    def __str__(self):
        return self.priceByQuantity

    class Meta:
        ordering = ['priceByQuantity']