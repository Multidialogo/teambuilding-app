from django.shortcuts import render


def home(request):
    text = ''
    return render(request, 'teambuilding/shared/welcome.html', {'text': text})
