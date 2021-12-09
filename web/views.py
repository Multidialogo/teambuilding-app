from django.shortcuts import render


def home(request):
    text = ''
    return render(request, 'welcome.html', {'text': text})
