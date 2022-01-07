from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404

from apps.events.forms import TasteEventForm
from apps.events.models import TasteEvent
from apps.events.events import on_taste_event_created


@login_required
def list_upcoming_by_all(request):
    now = datetime.now()
    events = TasteEvent.objects.filter(end_date__gte=now)
    context = {'events': events}
    return render(request, 'event/list_upcoming_by_all.html', context)


@login_required
def list_past_by_all(request):
    now = datetime.now()
    events = TasteEvent.objects.filter(end_date__lt=now)
    context = {'events': events}
    return render(request, 'event/list_past_by_all.html', context)


@login_required
def list_upcoming_by_self(request):
    events = TasteEvent.objects.filter(organizer=request.user)
    context = {'events': events}
    return render(request, 'event/list_upcoming_by_self.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = TasteEventForm(request.POST)
        form.instance.organizer = request.user

        if form.is_valid():
            event = form.save()

            on_taste_event_created(request, event)
            return redirect('event-user-list')
    else:
        form = TasteEventForm()

    context = {'event_form': form}
    return render(request, 'event/create.html', context)


@login_required
def detail(request, pk):
    event = get_object_or_404(TasteEvent, pk=pk)
    context = {'event': event}
    return render(request, 'event/detail.html', context)


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

    context = {'form': form}
    return render(request, 'apps/events/edit.html', context)


@login_required
def delete(request, pk):
    event = get_object_or_404(TasteEvent, pk=pk)

    if event.organizer.id != request.user.id:
        raise PermissionDenied()

    if request.method == 'POST':
        event.delete()
        return redirect('event-user-list')

    context = {'event': event}
    return render(request, 'event/delete.html', context)
