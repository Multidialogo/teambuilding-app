from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from events.forms import CreateEventForm
from events.models import TasteAndPurchaseEvent


@login_required
def redirect_manage_own_events(request):
    return redirect('manage_own_events')

@login_required
def manage_own_events(request):
    own_events = list(TasteAndPurchaseEvent.objects.filter(organizer=request.user))
    return render(request, 'manage_events.html', { 'events': own_events })

@login_required
def past_events(request):
    today = datetime.today()
    past_events = list(TasteAndPurchaseEvent.objects.filter(end_date__lt=today))
    return render(request, 'past_events.html', { 'events': past_events })

@login_required
def future_events(request):
    today = datetime.today()
    future_events = list(TasteAndPurchaseEvent.objects.filter(end_date__gte=today))
    return render(request, 'future_events.html', { 'events': future_events })

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