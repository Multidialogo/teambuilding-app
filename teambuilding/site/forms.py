from django import forms

from .models import User, HappyBirthdayMessage


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('account',)


class HappyBirthdayForm(forms.ModelForm):
    class Meta:
        model = HappyBirthdayMessage
        exclude = ('created_at', 'read', )
