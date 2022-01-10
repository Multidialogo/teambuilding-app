from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', verbose_name=_("account")
    )

    class Meta:
        verbose_name = _("user profile")
        verbose_name_plural = _("user profiles")

    def __str__(self):
        return str(self.account)
