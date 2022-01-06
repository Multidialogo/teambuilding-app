from django import forms

from ..products.models import ProductPurchaseOption, Product

from .models import ProducerOrder, ProducerOrderDeliveryAddress, OrderV2


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
