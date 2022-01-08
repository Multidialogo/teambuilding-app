from django import forms

from .models import TasteEvent


class TasteEventForm(forms.ModelForm):
    class Meta:
        model = TasteEvent
        exclude = ('organizer',)
