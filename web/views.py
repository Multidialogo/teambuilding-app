from django.shortcuts import render


def home(request):
    text = ''
    return render(request, 'shared/welcome.html', {'text': text})
