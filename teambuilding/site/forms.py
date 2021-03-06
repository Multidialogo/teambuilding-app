from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext, gettext_lazy as _

from .models import HappyBirthdayMessage, Event


class RegistrationForm(UserCreationForm):
    nickname = forms.CharField(label=_("Nickname"), required=False)

    class Meta:
        model = get_user_model()
        fields = ("nickname", "email", "birth_date")

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # necessario sovrascrivere fields['password2'].label per
        # avere la traduzione
        self.fields['password2'].label = gettext('Password (confirm)')


class UserNicknameForm(forms.ModelForm):
    nickname = forms.CharField(label=_("Nickname"), required=False)

    class Meta:
        model = get_user_model()
        fields = ('nickname',)


class HappyBirthdayForm(forms.ModelForm):
    class Meta:
        model = HappyBirthdayMessage
        exclude = ('created_at', 'read', )


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ()
