from django.dispatch import receiver

from teambuilding.products.tasks import send_order_email_to_producer
from teambuilding.products.signals import producer_order_form_transaction_done


@receiver(producer_order_form_transaction_done)
def on_producer_order_form_transaction_done(**kwargs):
    order = kwargs['instance']
    producer = order.producer

    if producer.email:
        send_order_email_to_producer(producer.email, order)
