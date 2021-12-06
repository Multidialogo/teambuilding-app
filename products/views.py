from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from products.forms import AddProducerForm


@login_required
def add_producer(request):
    if request.method == 'POST':
        form = AddProducerForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('add_producer')
    else:
        form = AddProducerForm()

    return render(request, 'add_producer.html', {'form': form})
