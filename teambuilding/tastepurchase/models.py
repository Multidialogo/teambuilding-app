from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _, gettext

from lib.phonenumber.modelfields import PhoneNumberField

from lib.postaladdress.models import PostalAddress
from teambuilding.site.models import UserProfile


class ProducerPostalAddress(PostalAddress):
    class Meta:
        verbose_name = _("postal address")
        verbose_name_plural = _("postal addresses")


class Producer(models.Model):
    name = models.CharField(_("name"), max_length=50, unique=True)
    email = models.EmailField(_("email"), blank=True)
    phone = PhoneNumberField(_("phone number"), blank=True)
    added_by_user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, verbose_name=_("added by")
    )
    postal_address = models.OneToOneField(
        ProducerPostalAddress, on_delete=models.CASCADE, related_name='producer',
        verbose_name=_("postal address")
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
    added_by_user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, verbose_name=_("added by")
    )

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
        UserProfile, on_delete=models.CASCADE, related_name='+', verbose_name=_("customer")
    )
    producer = models.ForeignKey(
        Producer, on_delete=models.CASCADE, related_name='product_order',
        verbose_name=_("producer")
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_order', verbose_name=_("product")
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_CREATED,
        verbose_name=_("order status")
    )

    class Meta:
        ordering = ['producer', 'product']
        verbose_name = _("simple order")
        verbose_name_plural = _("simple orders")

    def __str__(self):
        return gettext(
            "Product: %(product)s, Producer: %(producer)s, Amount: %(amount)s, EUR (cents): %(price)01.0f, "
            "Customer email: %(customer-email)s"
        ) % ({
            'product': str(self.product), 'producer': str(self.producer), 'amount': self.purchase_option.amount,
            'price': self.purchase_option.price_cents, 'customer-email': self.customer.account.email
        })

    def clean(self):
        super().clean()

        self.producer = self.purchase_option.product.producer
        self.product = self.purchase_option.product

        if self.producer_order:
            if self.producer_order.producer.id != self.producer.id:
                raise ValidationError(
                    gettext("Producer in instance ProductOrder must be equal to Producer in instance ProducerOrder.")
                )

            self.status = ProductOrder.STATUS_PROCESSED
        else:
            self.status = ProductOrder.STATUS_CREATED


class TasteEvent(models.Model):
    start_date = models.DateTimeField(_("event start"), help_text=_("Format: dd/mm/YYYY hh:mm"))
    end_date = models.DateTimeField(_("event end"), help_text=_("Format: dd/mm/YYYY hh:mm"))
    title = models.CharField(_("title"), max_length=50)
    description = models.CharField(_("description"), max_length=100)
    organizer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name=_("organizer"))
    products = models.ManyToManyField(Product, verbose_name=_("products"))

    class Meta:
        ordering = ['start_date', 'title']
        verbose_name = _("taste event")
        verbose_name_plural = _("taste events")

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.start_date > self.end_date:
            raise ValidationError({
                'start_date': gettext("End date must come after start date."),
                'end_date': gettext("End date must come after start date.")
            })
