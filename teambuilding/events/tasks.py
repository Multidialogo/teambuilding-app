import sys
from tempfile import NamedTemporaryFile

from django.core.mail import EmailMessage

from teambuilding.users.models import User

from .utils import create_icalendar_from_taste_event


def notify_new_taste_event_to_all_users(taste_event):
    icalendar = create_icalendar_from_taste_event(taste_event)
    mail_subject = 'Nuovo evento Taste & Purchase!'
    message = 'Un nuovo evento è stato aggiunto.'
    emails = User.objects.values_list('account__email', flat=True)

    with NamedTemporaryFile(mode='w+b') as ics:
        ics.write(icalendar)
        ics.seek(0)
        ics_content = ics.read()

        email = EmailMessage(mail_subject, message, to=emails)
        email.attach('event.ics', ics_content, 'application/octet-stream')
        email.send()
