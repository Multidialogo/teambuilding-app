from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from apps.products.forms import ProductForm, ProducerForm, ProducerPostalAddressFormsetFactory, \
    ProductPurchaseOptionFormsetFactory
from apps.products.models import Product, Producer
from services.postal_address.models import Country


@login_required
def list_manage(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'apps/products/list_manage.html', context)


@login_required
def add(request):
    purchase_option_formset_factory = ProductPurchaseOptionFormsetFactory(1)
    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save(commit=False)
            options_formset = purchase_option_formset_factory.make(request.POST, instance=product)

            if options_formset.is_valid():
                form.save()
                options_formset.save()
                return redirect('product-list-manage')
        else:
            options_formset = purchase_option_formset_factory.make(request.POST)
    else:
        form = ProductForm()
        options_formset = purchase_option_formset_factory.make(instance=form.instance)

    options_formset_config = {
        'title': 'Purchase options',
        'model_name': 'productpurchaseoption',
        'min_num': purchase_option_formset_factory.min_num
    }

    options_formset_meta = {'config': options_formset_config, 'formset': options_formset}
    context = {'form': form, 'formsets': (options_formset_meta,)}
    return render(request, 'apps/products/add.html', context)


@login_required
def edit(request, pk):
    purchase_option_formset_factory = ProductPurchaseOptionFormsetFactory(1)
    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save(commit=False)
            options_formset = purchase_option_formset_factory.make(request.POST, instance=product)

            if options_formset.is_valid():
                form.save()
                options_formset.save()
                return redirect('product-list-manage')
        else:
            options_formset = purchase_option_formset_factory.make(request.POST)
    else:
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(instance=product)
        options_formset = purchase_option_formset_factory.make(instance=product)

    options_formset_config = {
        'title': 'Purchase options',
        'model_name': 'productpurchaseoption',
        'min_num': purchase_option_formset_factory.min_num
    }

    options_formset_meta = {'config': options_formset_config, 'formset': options_formset}
    context = {'form': form, 'formsets': (options_formset_meta,)}
    return render(request, 'apps/products/edit.html', context)


@login_required
def delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('product-list-manage')

    context = {'product': product}
    return render(request, 'apps/products/delete.html', context)


@login_required
def producer_list_manage(request):
    producers = Producer.objects.all()
    context = {'producers': producers}
    return render(request, 'apps/products/producer_list_manage.html', context)


@login_required
def producer_add(request, country=None):
    address_formset_factory = ProducerPostalAddressFormsetFactory()
    if request.method == 'POST':
        form = ProducerForm(request.POST)

        if form.is_valid():
            producer = form.save(commit=False)
            address_formset = address_formset_factory.make(country, request.POST, producer)

            if address_formset.is_valid():
                form.save()
                address_formset.save()
                return redirect('product-producer-list-manage')
        else:
            address_formset = address_formset_factory.make(country, request.POST)
    else:
        form = ProducerForm()
        address_formset = address_formset_factory.make(country, instance=form.instance)

    address_formset_config = {
        'model_name': 'producerpostaladdress'
    }

    address_formset_meta = {'config': address_formset_config, 'formset': address_formset}
    context = {'form': form, 'formsets': (address_formset_meta,)}
    return render(request, 'apps/products/producer_add.html', context)


@login_required
def producer_edit(request, pk, country=None):
    address_formset_factory = ProducerPostalAddressFormsetFactory()
    producer = get_object_or_404(Producer, pk=pk)

    if request.method == 'POST':
        form = ProducerForm(request.POST, instance=producer)

        if form.is_valid():
            producer = form.save(commit=False)
            country = producer.producerpostaladdress.country.country_code
            address_formset = address_formset_factory.make(country, request.POST, producer)

            if address_formset.is_valid():
                form.save()
                address_formset.save()
                return redirect('product-producer-list-manage')
        else:
            country = producer.producerpostaladdress.country.country_code
            address_formset = address_formset_factory.make(country, request.POST, producer)
    else:
        form = ProducerForm(instance=producer)
        country = country or producer.producerpostaladdress.country.country_code
        address_formset = address_formset_factory.make(country, instance=producer)

    address_formset_config = {
        'model_name': 'producerpostaladdress'
    }

    debug_text = country
    address_formset_meta = {'config': address_formset_config, 'formset': address_formset}
    context = {'form': form, 'formsets': (address_formset_meta,), 'debug_text': debug_text}
    return render(request, 'apps/products/producer_edit.html', context)


@login_required
def producer_delete(request, pk):
    producer = get_object_or_404(Producer, pk=pk)

    if request.method == 'POST':
        producer.delete()
        return redirect('product-producer-list-manage')

    context = {'producer': producer}
    return render(request, 'apps/products/producer_delete.html', context)
