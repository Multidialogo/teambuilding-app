from lib.form_utils.forms import BaseModelForm
from .models import TasteEvent


class TasteEventForm(BaseModelForm):
    class Meta:
        model = TasteEvent
        exclude = ('organizer',)
