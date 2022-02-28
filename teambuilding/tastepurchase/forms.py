from django import forms

from .models import (
    Producer, Product, ProductPurchaseOption, ProducerPostalAddress, ProductOrder, ProducerOrder,
    ProducerOrderDeliveryAddress, TasteEvent
)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()


class ProductPurchaseOptionForm(forms.ModelForm):
    class Meta:
        model = ProductPurchaseOption
        exclude = ()


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
        exclude = ('producer_order', 'producer', 'product', 'status')


class ProducerOrderForm(forms.ModelForm):
    class Meta:
        model = ProducerOrder
        exclude = ('address',)


class ProducerOrderDeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = ProducerOrderDeliveryAddress
        exclude = ('order',)


class TasteEventForm(forms.ModelForm):
    class Meta:
        model = TasteEvent
        exclude = ()
