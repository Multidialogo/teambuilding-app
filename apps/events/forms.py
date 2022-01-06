from django import forms

from .models import TasteEvent


class TasteEventForm(forms.ModelForm):
    class Meta:
        model = TasteEvent
        fields = ('title', 'description', 'products', 'start_date', 'end_date',)
