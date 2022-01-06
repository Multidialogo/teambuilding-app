from django import forms
from django.shortcuts import get_object_or_404

from .models import Producer, Product, ProductPurchaseOption, ProducerPostalAddress


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields['producer'].empty_label = None


class ProductPurchaseOptionForm(forms.ModelForm):
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


class ProducerForm(forms.ModelForm):
    class Meta:
        model = Producer
        exclude = ()


class ProducerPostalAddressForm(forms.ModelForm):
    class Meta:
        model = ProducerPostalAddress
        exclude = ('producer',)
