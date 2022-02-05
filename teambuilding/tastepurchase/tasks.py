from tempfile import NamedTemporaryFile

from django.core.mail import send_mail, EmailMessage
from django.utils.translation import gettext

from .models import ProductOrder
from .utils import create_icalendar_from_taste_event


def send_order_email_to_producer(order):
    small_orders = ProductOrder.objects.filter(producer_order_id=order.id)
    email = order.producer.email
    receipt = ""

    for small_order in small_orders:
        receipt = receipt + "- " + "%(order)s" % ({'order': str(small_order)}) + "\n"

    message = gettext("Orders:\n%(receipt)s\nDelivery address:\n%(address)s") % (
        {'receipt': receipt, 'address': str(order.address)}
    )

    send_mail(
        gettext("New order"),
        message,
        None,
        [email],
        fail_silently=True
    )


def email_taste_event_notification(notification, taste_event):
    icalendar = create_icalendar_from_taste_event(taste_event)
    mail_subject = gettext("New event Taste & Purchase!")
    message = gettext("A new event has been added, check it out.")
    recipient_email = notification.recipient.email

    with NamedTemporaryFile(mode='w+b') as ics:
        ics.write(icalendar)
        ics.seek(0)
        ics_content = ics.read()

        email = EmailMessage(mail_subject, message, to=[recipient_email])
        email.attach('event.ics', ics_content, 'application/octet-stream')
        email.send()
