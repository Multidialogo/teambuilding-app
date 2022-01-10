from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _, gettext

from phonenumber_field.modelfields import PhoneNumberField

from lib.postaladdress.models import PostalAddress
from teambuilding.users.models import User


class ProducerPostalAddress(PostalAddress):
    class Meta:
        verbose_name = _("postal address")
        verbose_name_plural = _("postal addresses")


class Producer(models.Model):
    name = models.CharField(_("name"), max_length=50, unique=True)
    email = models.EmailField(_("email"), blank=True)
    phone = PhoneNumberField(_("phone number"), blank=True)
    postal_address = models.OneToOneField(
        ProducerPostalAddress, on_delete=models.CASCADE, related_name='producer', verbose_name=_("postal address")
    )

    class Meta:
        ordering = ['name']
        verbose_name = _("producer")
        verbose_name_plural = _("producers")

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(_("name"), max_length=50, unique=True)
    description = models.CharField(_("description"), max_length=100)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, verbose_name=_("producer"))

    class Meta:
        ordering = ['title']
        verbose_name = _("product")
        verbose_name_plural = _("products")

    def __str__(self):
        return self.title


class ProductPurchaseOption(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='purchase_option', verbose_name=_("product")
    )
    price_cents = models.IntegerField(_("price EUR (cents)"))
    amount = models.CharField(_("amount"), max_length=50)

    class Meta:
        unique_together = ('amount', 'product')
        ordering = ['price_cents']
        verbose_name = _("purchase option")
        verbose_name_plural = _("purchase options")

    def __str__(self):
        return gettext("Amount: %(amount)s, EUR (cents): %(price)01.0f") % (
            {'amount': self.amount, 'price': self.price_cents}
        )


class ProducerOrderDeliveryAddress(PostalAddress):
    class Meta:
        verbose_name = _("delivery address")
        verbose_name_plural = _("delivery addresses")


class ProducerOrder(models.Model):
    producer = models.ForeignKey(
        Producer, on_delete=models.CASCADE, related_name='producer_order', verbose_name=_("producer")
    )
    address = models.OneToOneField(
        ProducerOrderDeliveryAddress, on_delete=models.CASCADE, related_name='order', verbose_name=_("delivery address")
    )

    class Meta:
        verbose_name = _("cumulative order to producer")
        verbose_name_plural = _("cumulative orders to producers")

    def __str__(self):
        return gettext("cumulative order for producer %(producer)s") % ({'producer': self.producer})


class ProductOrder(models.Model):
    STATUS_CREATED = 'CREATED'
    STATUS_PROCESSED = 'PROCESSED'
    STATUS_CHOICES = [
        (STATUS_CREATED, _("Created")),
        (STATUS_PROCESSED, _("Processed"))
    ]

    purchase_option = models.ForeignKey(
        ProductPurchaseOption, on_delete=models.CASCADE, related_name='product_order',
        verbose_name=_("purchase option")
    )
    producer_order = models.ForeignKey(
        ProducerOrder, on_delete=models.CASCADE, null=True, related_name='product_order',
        verbose_name=_("in cumulative order")
    )
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='+', verbose_name=_("customer")
    )
    producer = models.ForeignKey(
        Producer, on_delete=models.CASCADE, related_name='product_order', verbose_name=_("producer")
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_order', verbose_name=_("product")
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_CREATED, verbose_name=_("order status")
    )

    class Meta:
        ordering = ['producer', 'product']
        verbose_name = _("simple order")
        verbose_name_plural = _("simple orders")

    def __str__(self):
        return gettext("Product: %(product)s, Amount: %(amount)s, EUR (cents): %(price)01.0f") % ({
            'product': str(self.product), 'amount': self.purchase_option.amount,
            'price': self.purchase_option.price_cents
        })

    def clean(self):
        super().clean()

        self.producer = self.purchase_option.product.producer
        self.product = self.purchase_option.product

        if self.producer_order:
            if self.producer_order.producer.id != self.producer.id:
                raise ValidationError(
                    gettext("Producer in instance ProductOrder must be equal to Producer in instance ProducerOrder."))

            self.status = ProductOrder.STATUS_PROCESSED
        else:
            self.status = ProductOrder.STATUS_CREATED
