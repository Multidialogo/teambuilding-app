from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from .forms import CreateEventForm
from .models import TasteAndPurchaseEvent


@login_required
def redirect_manage_own_events(request):
    return redirect('manage_own_events')


@login_required
def manage_own_events(request):
    own_events = list(TasteAndPurchaseEvent.objects.filter(organizer=request.user))
    return render(request, 'manage_events.html', {'events': own_events})


@login_required
def past_events(request):
    today = datetime.today()
    past_events_list = list(TasteAndPurchaseEvent.objects.filter(end_date__lt=today))
    return render(request, 'past_events.html', {'events': past_events_list})


@login_required
def future_events(request):
    today = datetime.today()
    future_events_list = list(TasteAndPurchaseEvent.objects.filter(end_date__gte=today))
    return render(request, 'future_events.html', {'events': future_events_list})


@login_required
def create_event(request):
    if request.method == 'POST':
        form = CreateEventForm(request.POST)
        form.instance.organizer = request.user

        if form.is_valid():
            event = form.save()
            event.notify_users()

            return redirect('profile')
    else:
        form = CreateEventForm()

    return render(request, 'create_event.html', {'form': form})


@login_required
def delete_event(request, pk):
    event = get_object_or_404(TasteAndPurchaseEvent, pk=pk)
    if request.method == 'POST':
        if event.organizer == request.user:
            event.delete()
        return redirect('manage_own_events')

    return render(request, 'delete_event.html', {'event': event})

