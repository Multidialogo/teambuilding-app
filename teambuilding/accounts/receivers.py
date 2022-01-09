from django.conf import settings
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import send_activation_mail_to_user


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def on_account_post_save(instance, created, **kwargs):
    if created:
        transaction.on_commit(
            lambda: send_activation_mail_to_user(instance, 'teambuilding.tasting.local')
        )
