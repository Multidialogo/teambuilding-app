from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from apps.events.forms import TasteEventForm
from apps.events.models import TasteAndPurchaseEvent


@login_required
def list_upcoming(request):
    today = datetime.today()
    events = TasteAndPurchaseEvent.objects.filter(end_date__gte=today)
    context = {'events': events}
    return render(request, 'apps/events/list_next.html', context)


@login_required
def list_history(request):
    today = datetime.today()
    events = TasteAndPurchaseEvent.objects.filter(end_date__lt=today)
    context = {'events': events}
    return render(request, 'apps/events/list_history.html', context)


@login_required
def list_manage(request):
    events = TasteAndPurchaseEvent.objects.filter(organizer=request.user)
    context = {'events': events}
    return render(request, 'apps/events/list_manage.html', context)


@login_required
def add(request):
    if request.method == 'POST':
        form = TasteEventForm(request.POST)
        form.instance.organizer = request.user

        if form.is_valid():
            event = form.save()
            event.notify_users()
            return redirect('events-list-manage')
    else:
        form = TasteEventForm()

    context = {'form': form}
    return render(request, 'apps/events/add.html', context)


@login_required
def detail(request, pk):
    event = get_object_or_404(TasteAndPurchaseEvent, pk=pk)
    context = {'event': event}
    return render(request, 'apps/events/detail.html', context)


@login_required
def edit(request, pk):
    event = get_object_or_404(TasteAndPurchaseEvent, pk=pk)
    if request.method == 'POST':
        form = TasteEventForm(request.POST, instance=event)

        if form.is_valid():
            form.save()
            return redirect('events-list-manage')
    else:
        form = TasteEventForm(instance=event)

    context = {'form': form}
    return render(request, 'apps/events/edit.html', context)


@login_required
def delete(request, pk):
    event = get_object_or_404(TasteAndPurchaseEvent, pk=pk)
    if event.organizer.id != request.user.id:
        # TODO / redirect to error page
        return redirect('events-list-manage')

    if request.method == 'POST':
        event.delete()
        return redirect('events-list-manage')

    context = {'event': event}
    return render(request, 'apps/events/delete.html', context)
