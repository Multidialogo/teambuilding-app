from datetime import datetime

from icalendar import Event, Calendar


def create_icalendar_from_event(event, calendar=None):
    calendar_event = Event()
    now = datetime.now()
    calendar_event.add('summary', event.description)
    calendar_event.add('dtstart', event.start_date)
    calendar_event.add('dtend', event.end_date)
    calendar_event.add('dtstamp', now)

    if not calendar:
        calendar = Calendar()

    calendar.add_component(calendar_event)
    return calendar.to_ical()

