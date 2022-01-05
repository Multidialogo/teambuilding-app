from django import forms
from django.forms.models import inlineformset_factory

from services.postal_address.localization import localize_formset
from services.postal_address.services import safe_country_code
from ..products.models import ProductPurchaseOption, Product

from .models import Order, ProducerOrder, ProducerOrderDeliveryAddress, OrderV2


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = OrderV2
        exclude = ('producerOrder', 'customer')

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id', None)
        super(PurchaseForm, self).__init__(*args, **kwargs)

        product = Product.objects.get(pk=product_id)
        self.initial['product'] = product
        self.fields['product'].empty_label = None
        self.fields['purchaseOption'].queryset = ProductPurchaseOption.objects.filter(product_id__exact=product_id)
        self.fields['purchaseOption'].empty_label = None


class ProducerOrderForm(forms.ModelForm):
    class Meta:
        model = ProducerOrder
        exclude = ('producer',)

    def __init__(self, *args, **kwargs):
        receipt = kwargs.pop('receipt', None)
        super(ProducerOrderForm, self).__init__(*args, **kwargs)

        self.initial['receipt'] = receipt
        self.fields['receipt'].disabled = True


class ProducerOrderDeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = ProducerOrderDeliveryAddress
        exclude = ('order',)

    def __init__(self, *arg, **kwarg):
        super(ProducerOrderDeliveryAddressForm, self).__init__(*arg, **kwarg)
        self.empty_permitted = False


class ProducerOrderDeliveryAddressFormsetFactory:
    def __init__(self, min_num=1, max_num=1):
        self.min_num = min_num
        self.max_num = max_num

    def make(self, country_code=None, request=None, instance=None, extra=0):
        builder = inlineformset_factory(
            ProducerOrder, ProducerOrderDeliveryAddress, form=ProducerOrderDeliveryAddressForm, min_num=self.min_num,
            validate_min=True, extra=extra, can_delete=False, max_num=self.max_num, validate_max=True
        )
        country_code = safe_country_code(country_code)
        raw = builder(request or None, instance=instance)
        return localize_formset(country_code, raw)
