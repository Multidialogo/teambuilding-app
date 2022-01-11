from copy import copy

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django import forms
from django.shortcuts import redirect, render, get_object_or_404

from lib.postaladdress.localization import localize_form
from lib.postaladdress.utils import is_country_code_valid, safe_country_code

from .models import Product, Producer, ProductPurchaseOption, ProductOrder
from .forms import (
    ProductForm, ProducerForm, ProductPurchaseOptionForm, ProducerPostalAddressForm,
    ProductOrderForm, ProducerOrderForm, ProducerOrderDeliveryAddressForm
)


@login_required
def list_all(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'teambuilding/product/list.html', context)


@login_required
def list_purchasable(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'teambuilding/product/list_purchasable.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        post = copy(request.POST)
        form = ProductForm(post)

        if form.is_valid():
            post.update({'product': form.instance})
            option_form = ProductPurchaseOptionForm(post)

            if option_form.is_valid():
                with transaction.atomic():
                    form.save()
                    option_form.save()

                return redirect('product-list')
        else:
            option_form = ProductPurchaseOptionForm(post)
    else:
        form = ProductForm()
        option_form = ProductPurchaseOptionForm()

    option_form.fields['product'].widget = forms.HiddenInput()
    context = {'product_form': form, 'option_form': option_form}
    return render(request, 'teambuilding/product/create.html', context)


@login_required
def update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            return redirect('product-list')
    else:
        form = ProductForm(instance=product)

    options = ProductPurchaseOption.objects.filter(product_id=pk)
    context = {'pk': pk, 'options': options, 'product_form': form}
    return render(request, 'teambuilding/product/update.html', context)


@login_required
def delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('product-list')

    context = {'product': product}
    return render(request, 'teambuilding/product/delete.html', context)


@login_required
def product_order_create(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductOrderForm(request.POST)
        form.instance.customer = request.user.profile

        if form.is_valid():
            form.save()
            return redirect('product-list-purchasable')
    else:
        form = ProductOrderForm()
        options = ProductPurchaseOption.objects.filter(product_id=pk)
        form.fields['purchase_option'].queryset = options

    context = {'product': product, 'order_form': form}
    return render(request, 'teambuilding/product-order/create.html', context)


@login_required
def producer_list_all(request):
    producers = Producer.objects.all()
    context = {'producers': producers}
    return render(request, 'teambuilding/product-producer/list.html', context)


@login_required
def producer_list_purchasable(request):
    producers = Producer.objects.filter(product_order__producer_order__isnull=True)
    context = {'producers': producers}
    return render(request, 'teambuilding/product-producer/list_purchasable.html', context)


@login_required
def producer_create(request, country=None):
    if not is_country_code_valid(country):
        country = safe_country_code(country)
        return redirect('product-producer-create', country=country)

    if request.method == 'POST':
        form = ProducerForm(request.POST)
        address_form = localize_form(country, ProducerPostalAddressForm(request.POST))

        if address_form.is_valid():
            form.instance.postal_address = address_form.instance

            if form.is_valid():
                with transaction.atomic():
                    address_form.save()
                    form.save()

                return redirect('product-producer-list')
    else:
        form = ProducerForm()
        address_form = localize_form(country, ProducerPostalAddressForm())

    context = {'producer_form': form, 'address_form': address_form}
    return render(request, 'teambuilding/product-producer/create.html', context)


@login_required
def producer_update(request, pk, country=None):
    producer = get_object_or_404(Producer, pk=pk)

    if not is_country_code_valid(country):
        country = safe_country_code(country, producer.postal_address.country.country_code)
        return redirect('product-producer-update', pk=pk, country=country)

    if request.method == 'POST':
        form = ProducerForm(request.POST, instance=producer)
        address_form = localize_form(country, ProducerPostalAddressForm(request.POST, instance=producer.postal_address))

        if form.is_valid() and address_form.is_valid():
            with transaction.atomic():
                form.save()
                address_form.save()

            return redirect('product-producer-list')
    else:
        form = ProducerForm(instance=producer)
        address_form = localize_form(country, ProducerPostalAddressForm(instance=producer.postal_address))

    context = {'pk': pk, 'producer_form': form, 'address_form': address_form}
    return render(request, 'teambuilding/product-producer/update.html', context)


@login_required
def producer_delete(request, pk):
    producer = get_object_or_404(Producer, pk=pk)

    if request.method == 'POST':
        producer.delete()
        return redirect('product-producer-list')

    context = {'producer': producer}
    return render(request, 'teambuilding/product-producer/delete.html', context)


@staff_member_required
def producer_order_create(request, producer_id, country=None):
    producer = get_object_or_404(Producer, pk=producer_id)

    if not is_country_code_valid(country):
        country = safe_country_code(country, producer.postal_address.country.country_code)
        return redirect('product-producer-order-create', producer_id=producer_id, country=country)

    orders = ProductOrder.objects.filter(producer_id=producer_id, producer_order__isnull=True)

    if request.method == 'POST':
        form = ProducerOrderForm(request.POST)
        form.instance.producer = producer
        address_form = localize_form(country, ProducerOrderDeliveryAddressForm(request.POST))

        if address_form.is_valid():
            form.instance.address = address_form.instance

            if form.is_valid():
                orders = ProductOrder.objects.filter(producer_id=producer_id, producer_order__isnull=True)

                with transaction.atomic():
                    address_form.save()
                    form.save()

                    for product_order in orders:
                        product_order.producer_order = form.instance
                        product_order.save()

                return redirect('product-producer-list-purchasable')
    else:
        form = ProducerOrderForm()
        address_form = localize_form(country, ProducerOrderDeliveryAddressForm())

    context = {
        'producer_id': producer_id, 'country': country, 'orders': orders, 'order_form': form,
        'address_form': address_form
    }
    return render(request, 'teambuilding/product-producer-order/create.html', context)


@login_required
def purchase_option_create(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        post = copy(request.POST)
        post.update({'product': product})
        form = ProductPurchaseOptionForm(post)

        if form.is_valid():
            form.save()
            return redirect('product-update', pk=product_id)
    else:
        form = ProductPurchaseOptionForm(initial={'product': product})

    form.fields['product'].widget.attrs['disabled'] = True
    context = {'option_form': form}
    return render(request, 'teambuilding/product-purchase-option/create.html', context)


@login_required
def purchase_option_update(request, pk, product_id=None):
    option = get_object_or_404(ProductPurchaseOption, pk=pk)

    if not product_id:
        product_id = option.product.id
        return redirect('product-purchase-option-update', pk=pk, product_id=product_id)

    if request.method == 'POST':
        post = copy(request.POST)
        # è necessario passare il prodotto perché il campo è disabilitato,
        # quindi il valore non e' presente nella richiesta POST
        post.update({'product': option.product})
        form = ProductPurchaseOptionForm(post, instance=option)

        if form.is_valid():
            form.save()
            return redirect('product-update', pk=product_id)
    else:
        form = ProductPurchaseOptionForm(instance=option)

    form.fields['product'].widget.attrs['disabled'] = True
    context = {'option_form': form}
    return render(request, 'teambuilding/product-purchase-option/update.html', context)


@login_required
def purchase_option_delete(request, pk, product_id=None):
    option = get_object_or_404(ProductPurchaseOption, pk=pk)

    if not product_id:
        product_id = option.product.id
        return redirect('product-purchase-option-delete', pk=pk, product_id=product_id)

    if request.method == 'POST':
        option.delete()
        return redirect('product-update', pk=product_id)

    context = {'option': option}
    return render(request, 'teambuilding/product-purchase-option/delete.html', context)
