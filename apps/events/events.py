from apps.events.services import notify_new_taste_event_to_all_users


def on_taste_event_created(taste_event):
    notify_new_taste_event_to_all_users(taste_event)
