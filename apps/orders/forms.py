from django import forms
from django.forms.models import inlineformset_factory

from ..products.models import ProductPurchaseOption

from .models import Order, ProducerOrder, ProducerOrderDeliveryAddress


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Order
        priceByQuantity = forms.ModelChoiceField(queryset=ProductPurchaseOption.objects.all())
        fields = ('priceByQuantity',)

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id', None)
        super(PurchaseForm, self).__init__(*args, **kwargs)
        self.fields['priceByQuantity'].queryset = ProductPurchaseOption.objects.filter(
            product_id__exact=product_id)


class ProducerOrderForm(forms.ModelForm):
    class Meta:
        model = ProducerOrder
        exclude = ('producer',)


class ProducerOrderDeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = ProducerOrderDeliveryAddress
        exclude = ('order',)

    def __init__(self, *arg, **kwarg):
        super(ProducerOrderDeliveryAddressForm, self).__init__(*arg, **kwarg)
        self.empty_permitted = False


ProducerOrderDeliveryAddressFormSet = inlineformset_factory(
    ProducerOrder,
    ProducerOrderDeliveryAddress,
    form=ProducerOrderDeliveryAddressForm,
    extra=1,
    can_delete=False
)
