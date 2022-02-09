from django.contrib.auth import get_user_model
from django.utils.translation import gettext

from teambuilding.site.tasks import create_notification, send_calendar_event_mail


def notify_taste_event_created(taste_event):
    subject = gettext("New event Taste & Purchase!")
    body = gettext("A new event has been added, check it out.")
    all_users = get_user_model().objects.all()

    for user in all_users:
        create_notification(user, subject, body)
        send_calendar_event_mail(user, subject, body, taste_event)
