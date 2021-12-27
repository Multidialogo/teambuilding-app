from django import forms
from django.forms.models import inlineformset_factory

from .models import Producer, Product, ProductPurchaseOption, ProducerPostalAddress


class ProductPurchaseOptionForm(forms.ModelForm):
    class Meta:
        model = ProductPurchaseOption
        fields = ('product', 'quantity', 'priceInCents')

    def __init__(self, *args, **kwargs):
        if 'product' in kwargs:
            product_in = kwargs.pop('product')
            super(ProductPurchaseOptionForm, self).__init__(*args, **kwargs)
            self.fields['product'].initial = product_in
        else:
            super(ProductPurchaseOptionForm, self).__init__(*args, **kwargs)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()


class PurchaseOptionForm(forms.ModelForm):
    class Meta:
        model = ProductPurchaseOption
        exclude = ('product',)

    def __init__(self, *arg, **kwarg):
        super(PurchaseOptionForm, self).__init__(*arg, **kwarg)
        self.empty_permitted = False


PurchaseOptionFormSet = inlineformset_factory(
    Product,
    ProductPurchaseOption,
    form=PurchaseOptionForm,
    extra=1,
    can_delete=False
)


class ProducerForm(forms.ModelForm):
    class Meta:
        model = Producer
        exclude = ()


class ProducerPostalAddressForm(forms.ModelForm):
    class Meta:
        model = ProducerPostalAddress
        exclude = ('producer',)

    def __init__(self, *arg, **kwarg):
        super(ProducerPostalAddressForm, self).__init__(*arg, **kwarg)
        self.empty_permitted = False


PostalAddressFormSet = inlineformset_factory(
    Producer,
    ProducerPostalAddress,
    form=ProducerPostalAddressForm,
    extra=1,
    can_delete=False
)
