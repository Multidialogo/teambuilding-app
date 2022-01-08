from django.shortcuts import render


def home(request):
    text = ''
    return render(request, 'app/welcome.html', {'text': text})
