from django import forms

from events.models import TasteAndPurchaseEvent


class CreateEventForm(forms.ModelForm):
    class Meta:
        model = TasteAndPurchaseEvent
        fields = ('title', 'description', 'product', 'start_date', 'end_date',)
