from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ProducerOrder
from .tasks import send_order_email_to_producer


@receiver(post_save, sender=ProducerOrder)
def on_producer_order_post_save(instance, created, **kwargs):
    if created:
        transaction.on_commit(
            lambda: send_order_email_to_producer(instance)
        )
