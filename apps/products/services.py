from django.core.mail import send_mail


def make_receipt(orders):
    receipt = 'Product, Quantity, Price, Customer'

    for order in orders:
        receipt = receipt + "\n%s, %s, %s, %s" % (
            str(order.purchaseOption.product), str(order.purchaseOption.quantity), str(order.purchaseOption.priceInCents),
            str(order.customer))

    return receipt


def send_order_email_to_producer(email, receipt):
    send_mail(
        'New order',
        receipt,
        None,
        [email],
        fail_silently=True
    )
