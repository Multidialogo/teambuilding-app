from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from apps.products.forms import ProductForm, PurchaseOptionFormSet
from apps.products.models import Product


@login_required
def list_manage(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'apps/products/list_manage.html', context)


@login_required
def add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        options_formset = PurchaseOptionFormSet(request.POST, instance=form.instance)

        if form.is_valid():
            product = form.save(commit=False)
            options_formset = PurchaseOptionFormSet(request.POST, instance=product)
            if options_formset.is_valid():
                form.save()
                options_formset.save()
                return redirect('products-list-manage')
    else:
        form = ProductForm()
        options_formset = PurchaseOptionFormSet(instance=form.instance)

    context = {'form': form, 'options_formset': options_formset}
    return render(request, 'apps/products/add.html', context)


@login_required
def edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            return redirect('products-list-manage')
    else:
        form = ProductForm(instance=product)

    context = {'form': form}
    return render(request, 'apps/products/edit.html', context)


@login_required
def delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('products-list-manage')

    context = {'product': product}
    return render(request, 'apps/products/delete.html', context)
