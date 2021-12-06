from django import forms

from events.models import TasteAndPurchaseEvent
from products.models import Product


class CreateEventForm(forms.ModelForm):

    class Meta:
        model = TasteAndPurchaseEvent
        product = forms.ModelChoiceField(queryset=Product.objects.all())
        fields = ('title', 'description', 'product', 'start_date', 'end_date',)
