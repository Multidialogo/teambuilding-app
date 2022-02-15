from django.utils.translation import gettext

from teambuilding.site.tasks import EventNotificationManager


class TasteEventNotificationManager(EventNotificationManager):
    def __init__(self):
        super().__init__(
            gettext("New event Taste & Purchase!"),
            gettext("A new event has been added, check it out.")
        )
