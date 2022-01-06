from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from apps.products.forms import ProductForm, ProducerForm, ProductPurchaseOptionForm, ProducerPostalAddressForm
from apps.products.models import Product, Producer, ProductPurchaseOption
from services.postal_address.localization import localize_form
from services.postal_address.services import is_country_code_valid, safe_country_code


@login_required
def list_manage(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'apps/products/list_manage.html', context)


@login_required
def add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        option_form = ProductPurchaseOptionForm(request.POST, exclude_product_field=True)

        if form.is_valid():
            product = form.save(commit=False)
            option_form.instance.product = product

            if option_form.is_valid():
                form.save()
                option_form.save()
                return redirect('product-list-manage')
    else:
        form = ProductForm()
        option_form = ProductPurchaseOptionForm(exclude_product_field=True)

    context = {'form': form, 'option_form': option_form}
    return render(request, 'apps/products/add.html', context)


@login_required
def edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            return redirect('product-list-manage')
    else:
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
    if not is_country_code_valid(country):
        country = safe_country_code(country)
        return redirect('product-producer-add', country=country)

    if request.method == 'POST':
        form = ProducerForm(request.POST)
        address_form = localize_form(country, ProducerPostalAddressForm(request.POST))

        if form.is_valid():
            producer = form.save(commit=False)
            address_form.instance.producer = producer

            if address_form.is_valid():
                form.save()
                address_form.save()
                return redirect('product-producer-list-manage')
    else:
        form = ProducerForm()
        address_form = localize_form(country, ProducerPostalAddressForm())

    context = {'country_code': country, 'producer_form': form, 'address_form': address_form}
    return render(request, 'apps/products/producer_add.html', context)


@login_required
def producer_edit(request, pk, country=None):
    if not is_country_code_valid(country):
        producer = get_object_or_404(Producer, pk=pk)
        country = producer.producerpostaladdress.country.country_code
        return redirect('product-producer-edit', pk=pk, country=country)

    producer = get_object_or_404(Producer, pk=pk)
    address = producer.producerpostaladdress

    if request.method == 'POST':
        form = ProducerForm(request.POST, instance=producer)
        address_form = localize_form(country, ProducerPostalAddressForm(request.POST, instance=address))

        if form.is_valid() and address_form.is_valid():
            form.save()
            address_form.save()
            return redirect('product-producer-list-manage')
    else:
        form = ProducerForm(instance=producer)
        address_form = localize_form(country, ProducerPostalAddressForm(instance=address))

    context = {'producer_id': pk, 'country_code': country, 'producer_form': form, 'address_form': address_form}
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
    option = get_object_or_404(ProductPurchaseOption, pk=pk)

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
