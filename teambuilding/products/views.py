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
        post_args = copy(request.POST)
        post_args.update({'added_by_user': request.user.profile})
        form = ProductForm(post_args)

        if form.is_valid():
            with transaction.atomic():
                product = form.save()
                post_args.update({'product': product})
                option_form = ProductPurchaseOptionForm(post_args)

                if option_form.is_valid():
                    option_form.save()
                    return redirect('product-list')
        else:
            option_form = ProductPurchaseOptionForm(post_args)
    else:
        form = ProductForm()
        option_form = ProductPurchaseOptionForm()

    form.fields['added_by_user'].widget = forms.HiddenInput()
    option_form.fields['product'].widget = forms.HiddenInput()
    context = {'product_form': form, 'option_form': option_form}
    return render(request, 'teambuilding/product/create.html', context)


@login_required
def update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        post_args = copy(request.POST)
        form = ProductForm(post_args, instance=product)

        if form.is_valid():
            form.save()
            return redirect('product-list')
    else:
        form = ProductForm(instance=product)

    options = ProductPurchaseOption.objects.filter(product_id=pk)
    form.fields['added_by_user'].widget = forms.HiddenInput()

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
        post_args = copy(request.POST)
        post_args.update({'customer': request.user.profile})
        form = ProductOrderForm(post_args)

        if form.is_valid():
            form.save()
            return redirect('product-list-purchasable')
    else:
        form = ProductOrderForm()

    options = ProductPurchaseOption.objects.filter(product_id=pk)
    form.fields['purchase_option'].queryset = options
    form.fields['customer'].widget = forms.HiddenInput()

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
        post_args = copy(request.POST)
        post_args.update({'added_by_user': request.user.profile})
        form = ProducerForm(post_args)
        address_form = ProducerPostalAddressForm(post_args)
        locale_address_form = localize_form(country, address_form)

        if locale_address_form.is_valid():
            with transaction.atomic():
                postal_address = locale_address_form.save()
                form.instance.postal_address = postal_address

                if form.is_valid():
                    form.save()
                    return redirect('product-producer-list')
    else:
        form = ProducerForm()
        # nota: la funzione localize_form si preoccupa di impostare
        # il valore di address_form.fields['country'].initial,
        # quindi non serve impostarlo esplicitamente qui
        address_form = ProducerPostalAddressForm()
        locale_address_form = localize_form(country, address_form)

    form.fields['added_by_user'].widget = forms.HiddenInput()
    context = {'producer_form': form, 'address_form': locale_address_form}
    return render(request, 'teambuilding/product-producer/create.html', context)


@login_required
def producer_update(request, pk, country=None):
    producer = get_object_or_404(Producer, pk=pk)

    if not is_country_code_valid(country):
        country = safe_country_code(country, producer.postal_address.country.country_code)
        return redirect('product-producer-update', pk=pk, country=country)

    if request.method == 'POST':
        post_args = copy(request.POST)

        form = ProducerForm(post_args, instance=producer)
        address_form = ProducerPostalAddressForm(post_args, instance=producer.postal_address)
        locale_address_form = localize_form(country, address_form)

        if form.is_valid() and locale_address_form.is_valid():
            with transaction.atomic():
                form.save()
                locale_address_form.save()

            return redirect('product-producer-list')
    else:
        form = ProducerForm(instance=producer)
        # nota: la funzione localize_form si preoccupa di impostare
        # il valore di address_form.fields['country'].initial,
        # quindi non serve impostarlo esplicitamente qui
        address_form = ProducerPostalAddressForm(instance=producer.postal_address)
        locale_address_form = localize_form(country, address_form)

    context = {'pk': pk, 'producer_form': form, 'address_form': locale_address_form}
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

    if request.method == 'POST':
        post_args = copy(request.POST)
        post_args.update({'producer': producer})

        form = ProducerOrderForm(post_args)
        address_form = ProducerOrderDeliveryAddressForm(post_args)
        locale_address_form = localize_form(country, address_form)

        if locale_address_form.is_valid():
            with transaction.atomic():
                address = locale_address_form.save()
                form.instance.address = address

                if form.is_valid():
                    form.save()
                    orders = ProductOrder.objects.filter(
                        producer_id=producer_id, producer_order__isnull=True
                    )

                    for product_order in orders:
                        product_order.producer_order = form.instance
                        product_order.save()

                    return redirect('product-producer-list-purchasable')
    else:
        form = ProducerOrderForm(initial={'producer': producer})
        address_form = ProducerOrderDeliveryAddressForm()
        locale_address_form = localize_form(country, address_form)

    orders = ProductOrder.objects.filter(producer_id=producer_id, producer_order__isnull=True)
    form.fields['producer'].widget = forms.HiddenInput()
    context = {
        'producer_id': producer_id, 'country': country, 'orders': orders,
        'order_form': form, 'address_form': locale_address_form
    }
    return render(request, 'teambuilding/product-producer-order/create.html', context)


@login_required
def purchase_option_create(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        post_args = copy(request.POST)
        post_args.update({'product': product})
        form = ProductPurchaseOptionForm(post_args)

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
        post_args = copy(request.POST)
        # è necessario passare il prodotto perché il campo è disabilitato,
        # quindi il valore non e' presente nella richiesta POST
        post_args.update({'product': option.product})
        form = ProductPurchaseOptionForm(post_args, instance=option)

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
