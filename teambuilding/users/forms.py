from django import forms

from teambuilding.accounts.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('nickname',)
