from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext

from teambuilding.site.models import Notification, UserProfile

from .models import ProducerOrder, TasteEvent
from .tasks import send_order_email_to_producer


@receiver(post_save, sender=ProducerOrder)
def on_producer_order_post_save(instance, created, **kwargs):
    if created:
        transaction.on_commit(
            lambda: send_order_email_to_producer(instance)
        )

@receiver(post_save, sender=TasteEvent)
def on_taste_event_post_save(instance, created, **kwargs):
    if created:
        subject = gettext("New event Taste & Purchase!")
        message = gettext("A new event has been added, check it out.")
        all_users = UserProfile.objects.all()

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
def on_notification_post_save(instance, created, **kwargs):
    if created and instance.send_email and instance.origin == TasteEvent.__name__:
        taste_event = TasteEvent.objects.get(pk=instance.origin_object_id)
        transaction.on_commit(
            lambda: email_taste_event_notification(instance, taste_event)
        )
