from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import create_user_profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile_on_user_created(instance, created, **kwargs):
    if created:
        create_user_profile(instance)
