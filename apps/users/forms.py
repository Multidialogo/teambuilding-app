from apps.accounts.models import User
from lib.form_utils.forms import BaseModelForm


class UserForm(BaseModelForm):
    class Meta:
        model = User
        fields = ('nickname',)
