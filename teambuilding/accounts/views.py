from gettext import gettext

from django.conf import settings
from django.contrib.auth import logout as logout_request, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode

from .forms import RegistrationForm
from .tasks import send_activation_mail_to_user


@login_required
def logout(request):
    logout_request(request)
    return redirect('home')


def signup(request):
    if request.user and request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                user_inactive = form.save()
                site_domain = get_current_site(request).domain
                send_activation_mail_to_user(user_inactive, site_domain)

            context = {'registered_user': user_inactive}
            return render(request, 'teambuilding/account/signup_success.html', context)
    else:
        form = RegistrationForm()

    context = {'signup_form': form}
    return render(request, 'teambuilding/account/signup.html', context)


def activate(request, uid_64, token):
    try:
        user_id = urlsafe_base64_decode(uid_64).decode()
        user = get_user_model().objects.get(pk=user_id)
    except(TypeError, ValueError, OverflowError, settings.AUTH_USER_MODEL.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if not user.is_active:
            user.is_active = True
            user.save()

        message = gettext("Your account has been activated.")
    else:
        message = gettext("Invalid link.")

    context = {'message': message}
    return render(request, 'teambuilding/account/activate.html', context)
