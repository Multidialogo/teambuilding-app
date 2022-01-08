from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from teambuilding.events.forms import TasteEventForm
from teambuilding.events.models import TasteEvent
from teambuilding.events.signals import taste_event_form_transaction_done


@login_required
def list_upcoming_by_all(request):
    now = datetime.now()
    events = TasteEvent.objects.filter(end_date__gte=now)
    context = {'events': events}
    return render(request, 'teambuilding/event/list_upcoming_by_all.html', context)


@login_required
def list_past_by_all(request):
    now = datetime.now()
    events = TasteEvent.objects.filter(end_date__lt=now)
    context = {'events': events}
    return render(request, 'teambuilding/event/list_past_by_all.html', context)


@login_required
def list_upcoming_by_self(request):
    events = TasteEvent.objects.filter(organizer=request.user)
    context = {'events': events}
    return render(request, 'teambuilding/event/list_upcoming_by_self.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = TasteEventForm(request.POST)
        form.instance.organizer = request.user

        if form.is_valid():
            with transaction.atomic():
                form.save()
                pre_taste_event_created.send(sender='', instance=form.instance)

            taste_event_form_transaction_done.send(sender='', instance=form.instance)
            return redirect('event-user-list')
    else:
        form = TasteEventForm()

    context = {'event_form': form}
    return render(request, 'teambuilding/event/create.html', context)


@login_required
def detail(request, pk):
    event = get_object_or_404(TasteEvent, pk=pk)
    context = {'event': event}
    return render(request, 'teambuilding/event/detail.html', context)


@login_required
def update(request, pk):
    event = get_object_or_404(TasteEvent, pk=pk)

    if request.method == 'POST':
        form = TasteEventForm(request.POST, instance=event)

        if form.is_valid():
            form.save()
            return redirect('event-user-list')
    else:
        form = TasteEventForm(instance=event)

    context = {'event_form': form}
    return render(request, 'teambuilding/event/update.html', context)


@login_required
def delete(request, pk):
    event = get_object_or_404(TasteEvent, pk=pk)

    if event.organizer.id != request.user.id:
        raise PermissionDenied()

    if request.method == 'POST':
        event.delete()
        return redirect('event-user-list')

    context = {'event': event}
    return render(request, 'teambuilding/event/delete.html', context)
