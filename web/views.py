from django.shortcuts import render

from web import settings


def home(request):
    text = settings.SECRET_KEY
    return render(request, 'welcome.html', {'text': text})
