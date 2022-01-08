from django.dispatch import receiver

from teambuilding.events.tasks import notify_new_taste_event_to_all_users
from teambuilding.events.signals import post_taste_event_created


@receiver(post_taste_event_created)
def on_post_event_created(**kwargs):
    taste_event = kwargs['instance']
    notify_new_taste_event_to_all_users(taste_event)
