from django.core.mail import send_mail
from django.utils.translation import gettext


def send_order_email_to_producer(order):
    email = order.producer.email
    receipt = "Receipt"
    message = "Receipt:\n%s\n\nDelivery address:\n%s" % (receipt, str(order.address))

    send_mail(
        'New order',
        message,
        None,
        [email],
        fail_silently=True
    )
