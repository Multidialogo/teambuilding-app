from django import forms

from products.models import ProductPurchaseOption
from orders.models import Order


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
