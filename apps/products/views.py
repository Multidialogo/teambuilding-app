from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from services.postal_address.localization import localize_formset
from services.postal_address.services import safe_country_code
from .forms import PostalAddressFormSet, ProducerForm, AddProductForm, ProductPurchaseOptionForm
from .models import Product, ProductPurchaseOption, Producer


@login_required
def add_product_purchase_option(request, prod_id=0):
    product = Product.objects.filter(id=prod_id).first()
    if request.method == 'POST':
        form = ProductPurchaseOptionForm(request.POST, product=product)

        if form.is_valid():
            form.save()
            return redirect('list_prod_purchase_opt')
    else:
        form = ProductPurchaseOptionForm(product=product)

    return render(request, 'add_product_purchase_option.html', {'form': form})


@login_required
def list_product_purchase_options(request, prod_id=0):
    product = Product.objects.filter(id=prod_id).first()
    if product:
        prod_purchase_opt_list = ProductPurchaseOption.objects.filter(product=product)
    else:
        prod_purchase_opt_list = ProductPurchaseOption.objects.all()
    return render(request, 'list_product_purchase_options.html', {'prod_purchase_opt_list': prod_purchase_opt_list})


@login_required
def update_product_purchase_option(request, prod_option_id):
    prod_purchase_option = get_object_or_404(ProductPurchaseOption, id=prod_option_id)
    if request.method == 'POST':
        form = ProductPurchaseOptionForm(request.POST, instance=prod_purchase_option)

        if form.is_valid():
            form.save()
            return redirect('list_prod_purchase_opt')
    else:
        form = ProductPurchaseOptionForm(instance=prod_purchase_option)

    return render(request, 'update_product_purchase_option.html', {'form': form})


@login_required
def delete_product_purchase_option(request, prod_option_id):
    prod_purchase_option = get_object_or_404(ProductPurchaseOption, id=prod_option_id)
    if request.method == 'POST':
        prod_purchase_option.delete()
        return redirect('list_prod_purchase_opt')

    return render(request, 'delete_product_purchase_option.html', {'prod_purchase_option': prod_purchase_option})


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
def update_product(request, prod_id):
    product = get_object_or_404(Product, id=prod_id)
    if request.method == 'POST':
        form = AddProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            return redirect('list_products')
    else:
        form = AddProductForm(instance=product)

    return render(request, 'update_product.html', {'form': form})


@login_required
def delete_product(request, prod_id):
    product = get_object_or_404(Product, id=prod_id)
    if request.method == 'POST':
        product.delete()
        return redirect('list_products')

    return render(request, 'delete_product.html', {'product': product})


@login_required
def producer_create(request, country_code):
    country_code = safe_country_code(country_code)

    if request.method == 'POST':
        form = ProducerForm(request.POST)
        address_formset = localize_formset(country_code, PostalAddressFormSet(instance=form.instance))

        if form.is_valid():
            producer = form.save(commit=False)
            address_formset = localize_formset(country_code, PostalAddressFormSet(request.POST, instance=producer))
            if address_formset.is_valid():
                form.save()
                address_formset.save()
                return redirect('list_producers')
    else:
        form = ProducerForm()
        address_formset = localize_formset(country_code, PostalAddressFormSet(instance=form.instance))

    return render(request, 'add_producer.html', {'form': form, 'address_formset': address_formset})


@login_required
def list_producers(request):
    producer_list = Producer.objects.all()
    return render(request, 'list_producers.html', {'producer_list': producer_list})


@login_required
def redirect_add_producer_it(request):
    return redirect('add_producer', country_code='IT')
