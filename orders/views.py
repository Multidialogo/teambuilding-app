from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from events.models import Product
from orders.forms import PurchaseForm


@login_required
def purchase(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(pk=product_id)
        form = PurchaseForm(request.POST, product_id=product_id)
        form.instance.product = product
        if form.is_valid():
            return redirect('purchase_success')
    else:
        form = PurchaseForm(product_id=product_id)
    return render(request, 'purchase.html', {'form': form})


@login_required
def purchase_success(request):
    return render(request, 'purchase_success.html', {})
