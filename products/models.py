from django.db import models
from django.core.exceptions import ValidationError

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


# TODO : refactor? move somewhere else?
def validate_zip_code(value):
    str_value = str(value)
    if not str_value.isdigit():
        raise ValidationError(
            '%(value)s is not a valid zip code',
            params={'value': value},
        )


class Producer(models.Model):
    name = models.CharField('Name', max_length=50, unique=True)
    email = models.EmailField('Email', blank=True)
    phone = PhoneNumberField('Phone number', blank=True)
    address_country = CountryField('Country')
    address_zip_code = models.CharField('Zip code', max_length=5, validators=[validate_zip_code])
    address_street = models.CharField('Street', max_length=100)
    address_adm_level_1 = models.CharField('Administrative Level 1', max_length=100, blank=True)
    address_adm_level_2 = models.CharField('Administrative Level 2', max_length=100, blank=True)
    address_adm_level_3 = models.CharField('Administrative Level 3', max_length=100, blank=True)
    address_adm_level_4 = models.CharField('Administrative Level 4', max_length=100, blank=True)
    address_adm_level_5 = models.CharField('Administrative Level 5', max_length=100, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField('Title', max_length=50, unique=True)
    description = models.CharField('Description', max_length=100)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, verbose_name='Producer')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class PriceByQuantity(models.Model):
    priceInCents = models.IntegerField('Price (cents)')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    quantity = models.CharField('Quantity', max_length=50)

    class Meta:
        unique_together = ('quantity', 'product')
        ordering = ['priceInCents']

    def __str__(self):
        price_in_cents_str = str(self.priceInCents)
        return "Quantity: %s, Price: %s" % price_in_cents_str, self.quantity
