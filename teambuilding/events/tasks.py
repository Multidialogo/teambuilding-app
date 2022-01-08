from tempfile import NamedTemporaryFile
from django.core.mail import EmailMessage

from teambuilding.accounts.models import User
from teambuilding.events.utils import create_icalendar_from_taste_event


def notify_new_taste_event_to_all_users(taste_event):
    icalendar = create_icalendar_from_taste_event(taste_event)
    mail_subject = 'A new Taste & Purchase event is listed!'
    message = 'A new Taste & Purchase event is listed!'
    users = User.objects.all()

    with NamedTemporaryFile(mode='w+b') as ics:
        ics.write(icalendar)
        ics.seek(0)
        ics_content = ics.read()

        email = EmailMessage(mail_subject, message, to=users)
        email.attach('event.ics', ics_content, 'application/octet-stream')
        email.send()
