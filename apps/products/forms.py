from django.http import Http404
from django.shortcuts import get_object_or_404

from lib.form_utils.forms import BaseModelForm
from .models import Producer, Product, ProductPurchaseOption, ProducerPostalAddress, ProductOrder, ProducerOrder, \
    ProducerOrderDeliveryAddress


class ProductForm(BaseModelForm):
    class Meta:
        model = Product
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields['producer'].empty_label = None


class ProductPurchaseOptionForm(BaseModelForm):
    class Meta:
        model = ProductPurchaseOption
        exclude = ()

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id', None)
        exclude_product_field = bool(kwargs.pop('exclude_product_field', False))
        super(ProductPurchaseOptionForm, self).__init__(*args, **kwargs)

        if product_id:
            product = get_object_or_404(Product, pk=product_id)
            self.initial['product'] = product
            self.fields['product'].disabled = True

        if exclude_product_field:
            del self.fields['product']


class ProducerForm(BaseModelForm):
    class Meta:
        model = Producer
        exclude = ()


class ProducerPostalAddressForm(BaseModelForm):
    class Meta:
        model = ProducerPostalAddress
        exclude = ('producer',)


class ProductOrderForm(BaseModelForm):
    class Meta:
        model = ProductOrder
        exclude = ('customer', 'producerOrder')

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id')
        super(ProductOrderForm, self).__init__(*args, **kwargs)

        if not Product.objects.filter(pk=product_id).exists():
            raise Http404

        self.fields['purchaseOption'].queryset = ProductPurchaseOption.objects.filter(product_id__exact=product_id)
        self.fields['purchaseOption'].empty_label = None


class ProducerOrderForm(BaseModelForm):
    class Meta:
        model = ProducerOrder
        exclude = ()

    def __init__(self, *args, **kwargs):
        receipt = kwargs.pop('receipt')
        super(ProducerOrderForm, self).__init__(*args, **kwargs)

        self.initial['receipt'] = receipt
        self.fields['receipt'].disabled = True


class ProducerOrderDeliveryAddressForm(BaseModelForm):
    class Meta:
        model = ProducerOrderDeliveryAddress
        exclude = ('order',)
