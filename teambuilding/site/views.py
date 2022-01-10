from django.shortcuts import render


def home(request):
    context = {}
    return render(request, 'teambuilding/site/welcome.html', context)
