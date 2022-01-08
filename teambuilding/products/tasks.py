from django.core.mail import send_mail


def send_order_email_to_producer(email, order):
    receipt = order.receipt
    delivery_address = order.producerorderdeliveryaddress
    message = "Receipt:\n%s\n\nDelivery address:\n%s" % (receipt, str(delivery_address))

    send_mail(
        'New order',
        message,
        None,
        [email],
        fail_silently=True
    )
