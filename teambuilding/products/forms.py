from django import forms

from .models import (
    Producer, Product, ProductPurchaseOption, ProducerPostalAddress, ProductOrder, ProducerOrder,
    ProducerOrderDeliveryAddress
)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()


class ProductPurchaseOptionForm(forms.ModelForm):
    class Meta:
        model = ProductPurchaseOption
        exclude = ('product',)


class ProducerForm(forms.ModelForm):
    class Meta:
        model = Producer
        exclude = ('postal_address',)


class ProducerPostalAddressForm(forms.ModelForm):
    class Meta:
        model = ProducerPostalAddress
        exclude = ()


class ProductOrderForm(forms.ModelForm):
    class Meta:
        model = ProductOrder
        exclude = ('customer', 'producer_order', 'producer', 'product', 'status')


class ProducerOrderForm(forms.ModelForm):
    class Meta:
        model = ProducerOrder
        exclude = ('producer', 'address')


class ProducerOrderDeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = ProducerOrderDeliveryAddress
        exclude = ('order',)
