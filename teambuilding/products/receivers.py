from django.dispatch import receiver

from teambuilding.products.tasks import send_order_email_to_producer
from teambuilding.products.signals import pre_producer_order_created, post_producer_order_created


@receiver(pre_producer_order_created)
def on_pre_producer_order_created(**kwargs):
    order = kwargs['instance']
    product_orders = kwargs['product_orders']

    for product_order in product_orders:
        product_order.producerOrder = order
        product_order.save()


@receiver(post_producer_order_created)
def on_post_producer_order_created(**kwargs):
    order = kwargs['instance']
    producer = kwargs['producer']

    if producer.email:
        send_order_email_to_producer(producer.email, order)
