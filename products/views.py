from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from products.forms import AddProducerForm


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
