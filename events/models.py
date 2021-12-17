from django.db import models
from django.core.mail import EmailMessage
from datetime import datetime

from icalendar import Calendar, Event
from tempfile import NamedTemporaryFile

from products.models import Product
from users.models import User


class TasteAndPurchaseEvent(models.Model):
    start_date = models.DateTimeField('Event starts')
    end_date = models.DateTimeField('Event ends')
    title = models.CharField('Title', max_length=50)
    description = models.CharField('Description', max_length=100)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Organizer')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')

    class Meta:
        ordering = ['start_date', 'title']

    def __str__(self):
        return self.title

    def notify_users(self):
        # TODO : metodo lungo, possibile refactoring
        event = Event()
        event.add('summary', self.description)
        event.add('dtstart', self.start_date)
        event.add('dtend', self.end_date)
        event.add('dtstamp', datetime.now())
        cal = Calendar()
        cal.add_component(event)
        mail_subject = 'A new Taste & Purchase event is listed!'
        message = 'A new Taste & Purchase event is listed!'
        listeners = User.objects.all()

        with NamedTemporaryFile(mode='w+b') as ics:
            ics.write(cal.to_ical())
            ics.seek(0)

            email = EmailMessage(mail_subject, message, to=list(listeners))
            email.attach('event.ics', ics.read(), 'application/octet-stream')
            email.send()
