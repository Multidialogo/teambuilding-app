from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext

from .models import TasteEvent
from .tasks import email_taste_event_notification
from ..site.models import Notification, UserProfile


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
