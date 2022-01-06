from django.db import models

from services.postal_address.models import PostalAddress
from services.users.models import User

from ..products.models import ProductPurchaseOption, Producer, Product


class ProducerOrder(models.Model):
    receipt = models.TextField()


class ProducerOrderDeliveryAddress(PostalAddress):
    order = models.OneToOneField(ProducerOrder, on_delete=models.CASCADE)


class OrderV2(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchaseOption = models.ForeignKey(ProductPurchaseOption, on_delete=models.CASCADE)
    producerOrder = models.ForeignKey(ProducerOrder, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['product', 'purchaseOption']

    def __str__(self):
        return "Product: %s, %s " % (str(self.product), str(self.purchaseOption))

    def get_status(self):
        if self.producerOrder:
            return 'PROCESSED'
        return 'CREATED'
