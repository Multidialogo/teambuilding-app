from django.shortcuts import render
from events import models
from users.models import User
from web import settings


def home(request):
    text = settings.SECRET_KEY
    return render(request, 'welcome.html', { 'text': text })
