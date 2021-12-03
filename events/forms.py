from django import forms
from .models import Product, TasteAndPurchaseEvent

class CreateEventForm(forms.ModelForm):

    class Meta:
        model = TasteAndPurchaseEvent
        product = forms.ModelChoiceField(queryset=Product.objects.all())
        fields = ('title', 'description', 'product', 'start_date', 'end_date')