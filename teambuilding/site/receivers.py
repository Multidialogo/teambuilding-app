from django.conf import settings
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Notification
from .tasks import create_user_profile, send_email_from_notification


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def on_account_post_save(instance, created, **kwargs):
    if created:
        create_user_profile(instance)


@receiver(post_save, sender=Notification)
def on_notification_post_save(instance, created, **kwargs):
    if created & instance.send_email:
        transaction.on_commit(
            lambda: send_email_from_notification(instance)
        )
