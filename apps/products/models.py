from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from lib.postaladdress.models import PostalAddress
from apps.accounts.models import User


class Producer(models.Model):
    name = models.CharField('Name', max_length=50, unique=True)
    email = models.EmailField('Email', blank=True)
    phone = PhoneNumberField('Phone number', blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ProducerPostalAddress(PostalAddress):
    producer = models.OneToOneField(Producer, on_delete=models.CASCADE)


class Product(models.Model):
    title = models.CharField('Title', max_length=50, unique=True)
    description = models.CharField('Description', max_length=100)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, verbose_name='Producer')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class ProductPurchaseOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    priceInCents = models.IntegerField('Price (cents)')
    quantity = models.CharField('Quantity', max_length=50)

    class Meta:
        unique_together = ('quantity', 'product')
        ordering = ['priceInCents']

    def __str__(self):
        return "Quantity: %s, Price (in cents): %01.0f" % (self.quantity, self.priceInCents)


class ProducerOrder(models.Model):
    receipt = models.TextField()


class ProducerOrderDeliveryAddress(PostalAddress):
    order = models.OneToOneField(ProducerOrder, on_delete=models.CASCADE)


class ProductOrder(models.Model):
    purchaseOption = models.ForeignKey(ProductPurchaseOption, on_delete=models.CASCADE)
    producerOrder = models.ForeignKey(ProducerOrder, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['purchaseOption']

    def __str__(self):
        return "Product: %s, Quantity: %s, Price: %s " % (
            self.purchaseOption.product.title, self.purchaseOption.quantity, str(self.purchaseOption.priceInCents))

    def get_status(self):
        if self.producerOrder:
            return 'PROCESSED'
        return 'CREATED'
