from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from services.postal_address.models import PostalAddress
from services.postal_address.validators import validate_zip_code


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
    priceInCents = models.IntegerField('Price (cents)')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    quantity = models.CharField('Quantity', max_length=50)

    class Meta:
        unique_together = ('quantity', 'product')
        ordering = ['priceInCents']

    def __str__(self):
        return "Quantity: %s, Price (in cents): %01.0f" % (self.quantity, self.priceInCents)
