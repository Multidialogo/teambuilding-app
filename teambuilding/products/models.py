from django.core.exceptions import ValidationError
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from lib.postaladdress.models import PostalAddress
from teambuilding.users.models import User


class ProducerPostalAddress(PostalAddress):
    class Meta:
        verbose_name = 'indirizzo'
        verbose_name_plural = 'indirizzi'


class Producer(models.Model):
    name = models.CharField('nome', max_length=50, unique=True)
    email = models.EmailField('email', blank=True)
    phone = PhoneNumberField('telefono', blank=True)
    postal_address = models.OneToOneField(ProducerPostalAddress, on_delete=models.CASCADE, related_name='producer', verbose_name='indirizzo')

    class Meta:
        ordering = ['name']
        verbose_name = 'produttore'
        verbose_name_plural = 'produttori'

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField('nome prodotto', max_length=50, unique=True)
    description = models.CharField('descrizione', max_length=100)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, verbose_name='produttore')

    class Meta:
        ordering = ['title']
        verbose_name = 'prodotto'
        verbose_name_plural = 'prodotti'

    def __str__(self):
        return self.title


class ProductPurchaseOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchase_option', verbose_name='prodotto')
    price_cents = models.IntegerField('prezzo EURO (cents)')
    quantity = models.CharField('quantità', max_length=50)

    class Meta:
        unique_together = ('quantity', 'product')
        ordering = ['price_cents']
        verbose_name = 'opzione di acquisto'
        verbose_name_plural = 'opzioni di acquisto'

    def __str__(self):
        return "Quantità: %s, EURO (cents): %01.0f" % (self.quantity, self.price_cents)


class ProducerOrderDeliveryAddress(PostalAddress):
    class Meta:
        verbose_name = 'indirizzo di consegna'
        verbose_name_plural = 'indirizzi di consegna'


class ProducerOrder(models.Model):
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, related_name='producer_order', verbose_name='produttore')
    address = models.OneToOneField(ProducerOrderDeliveryAddress, on_delete=models.CASCADE, related_name='order', verbose_name='indirizzo di consegna')

    class Meta:
        verbose_name = 'ordine complessivo a produttore'
        verbose_name_plural = 'ordini complessivi a produttore'

    def __str__(self):
        return "ordine per il produttore %s" % (str(self.producer),)


class ProductOrder(models.Model):
    STATUS_CREATED = 'CREATED'
    STATUS_PROCESSED = 'PROCESSED'
    STATUS_CHOICES = [
        (STATUS_CREATED, 'Created'),
        (STATUS_PROCESSED, 'Processed')
    ]

    purchase_option = models.ForeignKey(ProductPurchaseOption, on_delete=models.CASCADE, related_name='product_order', verbose_name='opzione di acquisto')
    producer_order = models.ForeignKey(ProducerOrder, on_delete=models.CASCADE, null=True, related_name='product_order', verbose_name='ordine padre')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', verbose_name='ordinante')
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, related_name='product_order', verbose_name='produttore')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_order', verbose_name='prodotto')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_CREATED, verbose_name='stato ordine')

    class Meta:
        ordering = ['producer', 'product']
        verbose_name = 'ordine semplice'
        verbose_name_plural = 'ordini semplici'

    def __str__(self):
        return "Prodotto: %s, Quantità: %s, Prezzo EURO (cents): %s " % (
            str(self.purchase_option.product), self.purchase_option.quantity, str(self.purchase_option.price_cents)
        )

    def clean(self):
        super().clean()

        self.producer = self.purchase_option.product.producer
        self.product = self.purchase_option.product

        if self.producer_order:
            if self.producer_order.producer.id != self.producer.id:
                raise ValidationError('I produttori nelle istanze ProductOrder e ProducerOrder devono corrispondere.')

            self.status = ProductOrder.STATUS_PROCESSED
        else:
            self.status = ProductOrder.STATUS_CREATED
