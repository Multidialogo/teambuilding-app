from django import forms

from .models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('account',)
