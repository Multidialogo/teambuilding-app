from datetime import datetime
from tempfile import NamedTemporaryFile

from django.core.mail import EmailMessage
from icalendar import Event, Calendar

from services.users.models import User


def create_ical_from_taste_event(taste_event, calendar=None):
    calendar_event = Event()
    calendar_event.add('summary', taste_event.description)
    calendar_event.add('dtstart', taste_event.start_date)
    calendar_event.add('dtend', taste_event.end_date)
    calendar_event.add('dtstamp', datetime.now())

    if not calendar:
        calendar = Calendar()

    calendar.add_component(calendar_event)
    return calendar.to_ical()


def notify_new_taste_event_to_all_users(taste_event):
    ical = create_ical_from_taste_event(taste_event)
    mail_subject = 'A new Taste & Purchase event is listed!'
    message = 'A new Taste & Purchase event is listed!'
    users = User.objects.all()

    with NamedTemporaryFile(mode='w+b') as ics:
        ics.write(ical)
        ics.seek(0)

        email = EmailMessage(mail_subject, message, to=users)
        email.attach('event.ics', ics.read(), 'application/octet-stream')
        email.send()
