from django.db import models

from services.postal_address.models import PostalAddress
from services.users.models import User

from ..products.models import ProductPurchaseOption, Producer


class ProducerOrder(models.Model):
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)


class ProducerOrderDeliveryAddress(PostalAddress):
    order = models.OneToOneField(ProducerOrder, on_delete=models.CASCADE)


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Customer')
    priceByQuantity = models.ForeignKey(ProductPurchaseOption, on_delete=models.CASCADE, verbose_name='Price by quantity')
    producerOrder = models.ForeignKey(ProducerOrder, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['priceByQuantity']

    def __str__(self):
        return self.priceByQuantity

    def get_status(self):
        if self.producerOrder:
            return 'PROCESSED'
        return 'CREATED'


