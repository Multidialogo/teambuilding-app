from django.contrib.auth.forms import UserCreationForm
from django import forms

from users.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    nickname = forms.CharField(label="Nickname", required=False)

    class Meta:
        model = User
        fields = ("nickname", "email",)


class ChangeNicknameForm(forms.ModelForm):
    nickname = forms.CharField(label="Nickname", required=False)

    class Meta:
        model = User
        fields = ("nickname",)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.nickname = self.cleaned_data['nickname']
        if commit:
            user.save()
        return user
