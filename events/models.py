from django.db import models
from users.models import User
from localflavor.us.models import USZipCodeField, USStateField
from phonenumber_field.modelfields import PhoneNumberField
from icalendar import Calendar, Event
from datetime import datetime
from tempfile import NamedTemporaryFile
from django.core.mail import EmailMessage
from web.settings import DEBUG


class Producer(models.Model):
    name = models.CharField('Name',max_length=50,unique=True)
    email = models.EmailField('Email',blank=True)
    phone = PhoneNumberField('Phone number',blank=True)
    address_zip_code = USZipCodeField('Zip code')
    address_city = models.CharField('City',max_length=100)
    address_state = USStateField('State',)
    address_street = models.CharField('Street',max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Product(models.Model):
    title = models.CharField('Title',max_length=50, unique=True)
    description = models.CharField('Description',max_length=100)
    producer = models.ForeignKey(Producer,on_delete=models.CASCADE, verbose_name='Producer')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class PriceByQuantity(models.Model):
    priceInCents = models.IntegerField('Price (cents)')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    quantity = models.CharField('Quantity',max_length=50)

    def __str__(self):
        return "Quantity: %s, Price: %s" % (str(self.priceInCents), self.quantity)

    class Meta:
        unique_together = ('quantity', 'product')
        ordering = ['priceInCents']


class TasteAndPurchaseEvent(models.Model):
    start_date = models.DateTimeField('Event starts')
    end_date = models.DateTimeField('Event ends')
    title = models.CharField('Title',max_length=50)
    description = models.CharField('Description',max_length=100)
    organizer = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='Organizer')
    product = models.ForeignKey(Product,on_delete=models.CASCADE, verbose_name='Product')

    def __str__(self):
        return self.title

    def notify_users(self):
        cal = Calendar()
        event = Event()
        event.add('summary', self.description)
        event.add('dtstart', self.start_date)
        event.add('dtend', self.end_date)
        event.add('dtstamp', datetime.now())
        cal.add_component(event)
        mail_subject = 'A new Taste & Purchase event is listed!'
        message = ''
        listeners = User.objects.all()
        #listeners = User.objects.exclude(email__exact=self.organizer.email)
        with NamedTemporaryFile(mode='w+b') as ics:
            ics.write(cal.to_ical())
            ics.seek(0)
            email = EmailMessage(mail_subject, message, to=list(listeners))
            email.attach('event.ics', ics.read(), 'application/octet-stream')
            email.send()
        return True

    class Meta:
        ordering = ['start_date', 'title']
