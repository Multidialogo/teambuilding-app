from datetime import datetime
from tempfile import NamedTemporaryFile

from django.core.mail import EmailMessage
from icalendar import Event, Calendar

from teambuilding.accounts.models import User


def create_icalendar_from_taste_event(taste_event, calendar=None):
    calendar_event = Event()
    now = datetime.now()
    calendar_event.add('summary', taste_event.description)
    calendar_event.add('dtstart', taste_event.start_date)
    calendar_event.add('dtend', taste_event.end_date)
    calendar_event.add('dtstamp', now)

    if not calendar:
        calendar = Calendar()

    calendar.add_component(calendar_event)
    return calendar.to_ical()


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
