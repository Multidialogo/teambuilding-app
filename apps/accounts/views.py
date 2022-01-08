from django.contrib.auth import logout as logout_request
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode

from .events import on_account_created
from .forms import RegistrationForm
from .models import User


@login_required
def logout(request):
    logout_request(request)
    return redirect('home')


def signup(request):
    if request.user and request.user.is_authenticated:
        context = {'user': request.user}
        return render(request, 'registration/signup_success.html', context)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            on_account_created(request, user)

            context = {'user': user}
            return render(request, 'registration/signup_success.html', context)
    else:
        form = RegistrationForm()

    context = {'signup_form': form}
    return render(request, 'registration/signup.html', context)


def activate(request, uid_64, token):
    try:
        user_id = urlsafe_base64_decode(uid_64).decode()
        user = User.objects.get(pk=user_id)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if not user.is_active:
            user.is_active = True
            user.save()
            message = 'Email confirmed. You can now login.'
        else:
            message = 'Email already confirmed.'
    else:
        message = 'Invalid activation link.'

    context = {'message': message}
    return render(request, 'registration/activate.html', context)
