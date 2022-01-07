from apps.products.services import send_order_email_to_producer


def on_producer_order_created(request, order, producer, product_orders):
    if not request.method == 'POST':
        raise Exception('Server error')

    for product_order in product_orders:
        product_order.producerOrder = order
        product_order.save()

    if producer.email:
        send_order_email_to_producer(producer.email, order.receipt)
