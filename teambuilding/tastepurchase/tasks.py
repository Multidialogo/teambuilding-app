from django.utils.translation import gettext

from teambuilding.site.tasks import create_event_notification_manager


def create_taste_event_notification_manager():
    event_noti_manager = create_event_notification_manager(
        gettext("New event Taste & Purchase!"),
        gettext("A new event has been added, check it out.")
    )
    return event_noti_manager
