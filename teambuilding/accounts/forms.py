from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


class RegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("nickname", "email",)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password2'].label = 'Password (conferma)'


class UserAccountForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('nickname',)
