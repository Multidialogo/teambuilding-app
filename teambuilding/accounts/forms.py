from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext, gettext_lazy as _


class RegistrationForm(UserCreationForm):
    nickname = forms.CharField(label=_("Nickname"), required=False)

    class Meta:
        model = get_user_model()
        fields = ("nickname", "email",)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password2'].label = gettext('Password (confirm)')


class UserAccountForm(forms.ModelForm):
    nickname = forms.CharField(label=_("Nickname"), required=False)

    class Meta:
        model = get_user_model()
        fields = ('nickname',)
