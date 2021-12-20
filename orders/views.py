from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from products.models import Product
from orders.models import Order
from orders.forms import PurchaseForm


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
