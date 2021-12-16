from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from products.forms import AddProducerForm, AddProductForm
from products.models import Product


@login_required
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('list_products')
    else:
        form = AddProductForm()

    return render(request, 'add_product.html', {'form': form})


@login_required
def list_products(request):
    product_list = Product.objects.all()
    return render(request, 'list_products.html', {'product_list': product_list})


@login_required
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = AddProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            return redirect('list_products')
    else:
        form = AddProductForm(instance=product)

    return render(request, 'update_product.html', {'form': form})


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('list_products')

    return render(request, 'delete_product.html', {'product': product})


@login_required
def add_producer(request, country):
    if request.method == 'POST':
        form = AddProducerForm(request.POST, country=request.POST.get('address_country'))

        if form.is_valid():
            form.save()
            return redirect('add_producer', country=request.POST.get('address_country'))
    else:
        form = AddProducerForm(country=country)

    return render(request, 'add_producer.html', {'form': form})


@login_required
def redirect_add_producer_it(request):
    return redirect('add_producer', country='IT')
