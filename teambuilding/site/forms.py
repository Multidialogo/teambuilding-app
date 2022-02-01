from django import forms

from .models import User, Notification


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('account',)


class HappyBirthdayForm(forms.ModelForm):
    class Meta:
        model = Notification
        exclude = ('created_at', 'read', )
