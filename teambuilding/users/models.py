from django.conf import settings
from django.db import models


class User(models.Model):
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', verbose_name='account')

    class Meta:
        verbose_name = 'profilo utente'
        verbose_name_plural = 'profili utenti'

    def __str__(self):
        return str(self.account)
