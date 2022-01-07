from apps.events.services import notify_new_taste_event_to_all_users


def on_taste_event_created(request, taste_event):
    if not request.method == 'POST':
        raise Exception('Server error')

    notify_new_taste_event_to_all_users(taste_event)
