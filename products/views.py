from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from products.forms import AddProducerForm, AddProductForm, ProductFlavourForm
from products.models import Product, PriceByQuantity


@login_required
def add_product_flavour(request, product_id=0):
    product = Product.objects.filter(id=product_id).first()
    if request.method == 'POST':
        form = ProductFlavourForm(request.POST, product=product)

        if form.is_valid():
            form.save()
            return redirect('list_product_flavours')
    else:
        form = ProductFlavourForm(product=product)

    return render(request, 'add_product_flavour.html', {'form': form})


@login_required
def list_product_flavours(request, product_id=0):
    product = Product.objects.filter(id=product_id).first()
    if product:
        product_flavour_list = PriceByQuantity.objects.filter(product=product)
    else:
        product_flavour_list = PriceByQuantity.objects.all()
    return render(request, 'list_product_flavours.html', {'product_flavours_list': product_flavour_list})


@login_required
def update_product_flavour(request, product_flavour_id):
    product_flavour = get_object_or_404(PriceByQuantity, id=product_flavour_id)
    if request.method == 'POST':
        form = ProductFlavourForm(request.POST, instance=product_flavour)

        if form.is_valid():
            form.save()
            return redirect('list_product_flavours')
    else:
        form = ProductFlavourForm(instance=product_flavour)

    return render(request, 'update_product_flavour.html', {'form': form})


@login_required
def delete_product_flavour(request, product_flavour_id):
    product_flavour = get_object_or_404(PriceByQuantity, id=product_flavour_id)
    if request.method == 'POST':
        product_flavour.delete()
        return redirect('list_product_flavours')

    return render(request, 'delete_product_flavour.html', {'product_flavour': product_flavour})


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
