from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext

from teambuilding.site.models import Notification

from .models import ProducerOrder, TasteEvent
from .tasks import send_order_email_to_producer, email_taste_event_notification


@receiver(post_save, sender=ProducerOrder)
def send_email_to_producer_on_order_created(instance, created, **kwargs):
    if created:
        transaction.on_commit(
            lambda: send_order_email_to_producer(instance)
        )


@receiver(post_save, sender=TasteEvent)
def notify_on_taste_event_created(instance, created, **kwargs):
    if created:
        subject = gettext("New event Taste & Purchase!")
        message = gettext("A new event has been added, check it out.")
        all_users = get_user_model().objects.all()

        for user in all_users:
            Notification.objects.create(
                origin=instance.__class__.__name__,
                origin_object_id=instance.pk,
                recipient=user,
                subject=subject,
                body=message,
                send_email=True,
            )


@receiver(post_save, sender=Notification)
def send_email_on_taste_event_notification(instance, created, **kwargs):
    if created and instance.send_email and instance.origin == TasteEvent.__name__:
        taste_event = TasteEvent.objects.get(pk=instance.origin_object_id)
        transaction.on_commit(
            lambda: email_taste_event_notification(instance, taste_event)
        )
