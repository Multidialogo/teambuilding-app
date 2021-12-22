from django import forms

from .models import TasteAndPurchaseEvent


class TasteEventForm(forms.ModelForm):
    class Meta:
        model = TasteAndPurchaseEvent
        fields = ('title', 'description', 'products', 'start_date', 'end_date',)
