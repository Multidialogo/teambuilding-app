from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _, gettext


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


class HappyBirthdayMessage(models.Model):
    created_at = models.DateField(auto_now_add=True)
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("recipient"),
        related_name="+"
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("sender"),
        related_name="+", null=True
    )
    message = models.TextField(_("body"), max_length=500)

    class Meta:
        unique_together = ['created_at', 'recipient', 'sender']
        ordering = ['created_at', 'recipient', 'sender']
        verbose_name = _("happy birthday message")
        verbose_name_plural = _("happy birthday messages")

    def __str__(self):
        return gettext("Happy birthday message from %(sender)s to %(recipient)s") % (
            {'sender': str(self.sender), 'recipient': str(self.recipient)}
        )


class Notification(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("recipient"))
    subject = models.CharField(_("subject"), max_length=80)
    body = models.TextField(_("body"), max_length=256)
    read = models.BooleanField(_("read"), default=False)
    send_email = models.BooleanField(_("also send email"), default=False)
    origin = models.CharField(_("origin"), max_length=50, editable=False, default="SYSTEM")
    origin_object_id = models.CharField(
        _("origin object id"), max_length=64, editable=False, blank=True, null=True
    )

    class Meta:
        ordering = ['created_at']
        verbose_name = _("notification")
        verbose_name_plural = _("notifications")

    def __str__(self):
        return self.subject
