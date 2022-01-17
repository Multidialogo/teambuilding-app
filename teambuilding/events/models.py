from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _, gettext

from teambuilding.site.models import User
from teambuilding.products.models import Product


class TasteEvent(models.Model):
    start_date = models.DateTimeField(_("event start"), help_text=_("Format: dd/mm/YYYY hh:mm"))
    end_date = models.DateTimeField(_("event end"), help_text=_("Format: dd/mm/YYYY hh:mm"))
    title = models.CharField(_("title"), max_length=50)
    description = models.CharField(_("description"), max_length=100)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("organizer"))
    products = models.ManyToManyField(Product, verbose_name=_("products"))

    class Meta:
        ordering = ['start_date', 'title']
        verbose_name = _("taste event")
        verbose_name_plural = _("taste events")

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.start_date > self.end_date:
            raise ValidationError({
                'start_date': gettext("End date must come after start date."),
                'end_date': gettext("End date must come after start date.")
            })
