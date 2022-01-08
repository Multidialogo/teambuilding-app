from django import forms

from apps.accounts.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('nickname',)
