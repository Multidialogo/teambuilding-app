from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from .models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    nickname = forms.CharField(label="Nickname", required=False)

    class Meta:
        model = User
        fields = ("nickname", "email",)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'input'})


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'input'})
