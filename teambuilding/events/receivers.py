from django.dispatch import receiver

from teambuilding.events.tasks import notify_new_taste_event_to_all_users
from teambuilding.events.signals import taste_event_form_transaction_done


@receiver(taste_event_form_transaction_done)
def on_taste_event_form_transaction_done(**kwargs):
    taste_event = kwargs['instance']
    notify_new_taste_event_to_all_users(taste_event)
