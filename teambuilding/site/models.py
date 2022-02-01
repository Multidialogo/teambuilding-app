from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile',
        verbose_name=_("account")
    )

    class Meta:
        verbose_name = _("user profile")
        verbose_name_plural = _("user profiles")

    def __str__(self):
        return str(self.account)


class Notification(models.Model):
    NOTITYPE_EVENT = 'EVENT'
    NOTITYPE_BIRTHDAY = 'BIRTHDAY'
    NOTITYPE_CHOICES = [
        (NOTITYPE_EVENT, _("Event")),
        (NOTITYPE_BIRTHDAY, _("Birthday"))
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("sender"),
        related_name="+", null=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("user notified"))
    subject = models.CharField(_("subject"), max_length=80)
    body = models.TextField(_("body"), max_length=256)
    read = models.BooleanField(_("read"), default=False)
    send_email = models.BooleanField(_("also send email"), default=False)
    type = models.CharField(
        _("notification type"), max_length=16, choices=NOTITYPE_CHOICES, default=NOTITYPE_EVENT
    )

    class Meta:
        verbose_name = _("notification")
        verbose_name_plural = _("notifications")

    def __str__(self):
        return "%(type)s : %(subject)s" % {
            'type': self.type,
            'subject': self.subject
        }
