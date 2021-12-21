from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from services.postal_address.localization import localize_formset
from ..products.models import Product, Producer
from .models import Order
from .forms import PurchaseForm, ProducerOrderForm, ProducerOrderDeliveryAddressFormSet


@login_required
def list_orders(request, producer_id):
    order_list = Order.objects.filter(priceByQuantity__product__producer_id__exact=producer_id)
    return render(request, 'list_orders.html', {'order_list': order_list})


@login_required
def purchase(request, product_id):
    if request.method == 'POST':
        form = PurchaseForm(request.POST, product_id=product_id)
        form.instance.customer = request.user
        if form.is_valid():
            form.save()
            return redirect('purchase_success')
    else:
        form = PurchaseForm(product_id=product_id)
    return render(request, 'purchase.html', {'form': form})


@login_required
def purchase_success(request):
    return render(request, 'purchase_success.html', {})


@login_required
def order_producer_create(request, producer):
    producer_inst = Producer.objects.get(pk=producer)
    country_code = producer_inst.producerpostaladdress.country.country_code
    order_list = list(Order.objects.filter(priceByQuantity__product__producer_id=producer).filter(producerOrder__isnull=True))

    if request.method == 'POST':
        form = ProducerOrderForm(request.POST)
        address_formset = localize_formset(country_code, ProducerOrderDeliveryAddressFormSet(instance=form.instance))

        if form.is_valid():
            producer_order = form.save(commit=False)
            producer_order.producer = producer_inst
            address_formset = localize_formset(country_code, ProducerOrderDeliveryAddressFormSet(request.POST, instance=producer_order))
            if address_formset.is_valid():
                form.save()
                address_formset.save()
                for order in order_list:
                    order.producerOrder = producer_order
                    order.save()
                if producer_inst.email:
                    send_mail(
                        'New order',
                        'Placeholder message. Contact an admin.',
                        None,
                        [producer_inst.email],
                        fail_silently=True
                    )
                return redirect('list_producers')
    else:
        form = ProducerOrderForm()
        address_formset = localize_formset(country_code, ProducerOrderDeliveryAddressFormSet(instance=form.instance))

    return render(request, 'add_producer_order.html', {'form': form, 'address_formset': address_formset, 'order_list': order_list})
