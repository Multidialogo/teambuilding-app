from django import forms

from events.models import PriceByQuantity
from orders.models import Order


class PurchaseForm(forms.ModelForm):

    class Meta:
        model = Order
        priceByQuantity = forms.ModelChoiceField(queryset=PriceByQuantity.objects.all())
        fields = ('priceByQuantity',)

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id', None)
        super(PurchaseForm, self).__init__(*args, **kwargs)
        self.fields['priceByQuantity'].queryset = PriceByQuantity.objects.filter(
            product_id__exact=product_id)
