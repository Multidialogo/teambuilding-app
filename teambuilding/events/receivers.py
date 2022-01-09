from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import TasteEvent
from .tasks import notify_new_taste_event_to_all_users


@receiver(post_save, sender=TasteEvent)
def on_taste_event_post_save(instance, created, **kwargs):
    if created:
        transaction.on_commit(
            lambda: notify_new_taste_event_to_all_users(instance)
        )
