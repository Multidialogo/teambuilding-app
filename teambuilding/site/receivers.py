from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from teambuilding.site.tasks import create_user_profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def on_account_post_save(instance, created, **kwargs):
    if created:
        create_user_profile(instance)
