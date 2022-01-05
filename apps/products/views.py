from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from apps.products.forms import ProductForm, ProducerForm, ProducerPostalAddressFormsetFactory, PurchaseOptionForm, \
    ProductPurchaseOptionForm
from apps.products.models import Product, Producer, ProductPurchaseOption


@login_required
def list_manage(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'apps/products/list_manage.html', context)


@login_required
def add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save(commit=False)
            option_form = PurchaseOptionForm(request.POST)
            option_form.instance.product = product

            if option_form.is_valid():
                form.save()
                option_form.save()
                return redirect('product-list-manage')
        else:
            option_form = PurchaseOptionForm(request.POST)
    else:
        form = ProductForm()
        option_form = PurchaseOptionForm()

    context = {'form': form, 'option_form': option_form}
    return render(request, 'apps/products/add.html', context)


@login_required
def edit(request, pk):
    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('product-list-manage')
    else:
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(instance=product)

    options = ProductPurchaseOption.objects.filter(product_id__exact=pk)
    context = {'product_id': pk, 'options': options, 'product_form': form}
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


@login_required
def purchase_option_add(request, product_id):
    if request.method == 'POST':
        form = ProductPurchaseOptionForm(request.POST, product_id=product_id)

        if form.is_valid():
            form.save()
            return redirect('product-edit', pk=product_id)
    else:
        form = ProductPurchaseOptionForm(product_id=product_id)

    context = {'option_form': form}
    return render(request, 'apps/products/purchase_option_add.html', context)


@login_required
def purchase_option_edit(request, product_id, pk):
    option = ProductPurchaseOption.objects.get(pk=pk)

    if request.method == 'POST':
        form = ProductPurchaseOptionForm(request.POST, instance=option, product_id=product_id)

        if form.is_valid():
            form.save()
            return redirect('product-edit', pk=product_id)
    else:
        form = ProductPurchaseOptionForm(instance=option, product_id=product_id)

    context = {'option_form': form}
    return render(request, 'apps/products/purchase_option_edit.html', context)


@login_required
def purchase_option_delete(request, product_id, pk):
    option = get_object_or_404(ProductPurchaseOption, pk=pk)

    if request.method == 'POST':
        option.delete()
        return redirect('product-edit', pk=product_id)

    context = {'option': option, 'product_id': product_id}
    return render(request, 'apps/products/purchase_option_delete.html', context)
