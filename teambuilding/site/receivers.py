from django.conf import settings
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext

from .models import Notification, HappyBirthdayMessage
from .tasks import create_user_profile, send_email_from_notification


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def on_account_post_save(instance, created, **kwargs):
    if created:
        create_user_profile(instance)


@receiver(post_save, sender=HappyBirthdayMessage)
def on_happy_birthday_message_post_save(instance, created, **kwargs):
    if created:
        subject = gettext("Happy birthday, %s!") % instance.recipient.account.nickname
        Notification.objects.create(
            origin=instance.__class__.__name__,
            origin_object_id=instance.pk,
            recipient=instance.recipient,
            subject=subject,
            body=instance.message,
            send_email=True
        )


@receiver(post_save, sender=Notification)
def on_notification_post_save(instance, created, **kwargs):
    if created and instance.send_email:
        if instance.origin == "SYSTEM" or instance.origin == HappyBirthdayMessage.__name__:
            transaction.on_commit(
                lambda: send_email_from_notification(instance)
            )
