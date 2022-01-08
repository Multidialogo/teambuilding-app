from datetime import datetime

from icalendar import Event, Calendar


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
