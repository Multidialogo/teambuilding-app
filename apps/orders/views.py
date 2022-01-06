from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from services.postal_address.localization import localize_form
from services.postal_address.services import is_country_code_valid, safe_country_code
from .forms import PurchaseForm, ProducerOrderForm, ProducerOrderDeliveryAddressForm
from .models import OrderV2
from .services import make_receipt, send_order_email_to_producer
from ..products.models import Product, Producer


@login_required
def purchase(request, product_id=None):
    if Product.objects.count() == 0:
        return redirect('product-list-manage')

    if not product_id:
        product = Product.objects.all().first()
        return redirect('orders-user-purchase', product_id=product.pk)

    if request.method == 'POST':
        form = PurchaseForm(request.POST, product_id=product_id)
        form.instance.customer = request.user

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PurchaseForm(product_id=product_id)

    return render(request, 'apps/orders/purchase.html', {'form': form})


@staff_member_required
def list_manage(request, producer_id=None):
    if Producer.objects.count() == 0:
        return redirect('product-producer-list-manage')

    if not producer_id:
        producer = Producer.objects.first()
        return redirect('orders-staff-list-manage', producer_id=producer.pk)

    producers = Producer.objects.all()
    orders = OrderV2.objects.filter(product__producer_id__exact=producer_id).filter(producerOrder__isnull=True)

    context = {'orders': orders, 'producers': producers, 'producer_id': producer_id}
    return render(request, 'apps/orders/list_manage.html', context)


@staff_member_required
def send_to_producer(request, producer_id, country=None):
    producer = get_object_or_404(Producer, pk=producer_id)

    if not is_country_code_valid(country):
        valid_country_code = safe_country_code(None)
        return redirect('orders-staff-send-to-producer', producer_id=producer_id, country=valid_country_code)

    user_orders = OrderV2.objects.filter(product__producer_id__exact=producer_id).filter(producerOrder__isnull=True)
    receipt = make_receipt(user_orders)

    if request.method == 'POST':
        form = ProducerOrderForm(request.POST, receipt=receipt)
        address_form = localize_form(country, ProducerOrderDeliveryAddressForm(request.POST))

        if form.is_valid():
            order = form.save(commit=False)
            address_form.instance.order = order

            if address_form.is_valid():
                form.save()
                address_form.save()

                for user_order in user_orders:
                    user_order.producerOrder = order
                    user_order.save()

                if producer.email:
                    send_order_email_to_producer(producer.email, receipt)

                return redirect('orders-staff-list-manage', producer_id=producer_id)
    else:
        form = ProducerOrderForm(receipt=receipt)
        form.instance.producer = producer
        address_form = localize_form(country, ProducerOrderDeliveryAddressForm())

    context = {'producer_id': producer_id, 'country': country, 'order_form': form, 'address_form': address_form}
    return render(request, 'apps/orders/send_to_producer.html', context)
