from django.shortcuts import render


def home(request):
    text = ''
    return render(request, 'web/welcome.html', {'text': text})
