from django.shortcuts import render

from web import settings


def home(request):
    text = ''
    return render(request, 'welcome.html', {'text': text})
