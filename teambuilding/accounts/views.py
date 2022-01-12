from copy import copy

from django.conf import settings
from django.contrib.auth import logout as logout_request, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext

from .forms import RegistrationForm
from .models import UserAccount
from .tasks import send_activation_mail_to_user, send_reset_password_mail_to_user


@login_required
def logout(request):
    logout_request(request)
    return redirect('home')


def signup(request):
    if request.user and request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        post_args = copy(request.POST)
        form = RegistrationForm(post_args)

        if form.is_valid():
            with transaction.atomic():
                user_inactive = form.save()
                site_domain = get_current_site(request).domain
                # l'invio della mail avviene all'interno della transazione
                # atomica, in modo che se ci sono problemi nell'invio della
                # mail, quindi l'utente non puo' registrarsi, il record
                # non viene inserito nel database
                send_activation_mail_to_user(user_inactive, site_domain)

            context = {'registered_user': user_inactive}
            return render(request, 'teambuilding/account/signup_success.html', context)
    else:
        form = RegistrationForm()

    context = {'signup_form': form}
    return render(request, 'teambuilding/account/signup.html', context)


def activate(request, uidb64, token):
    try:
        user_id = urlsafe_base64_decode(uidb64).decode()
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


def password_reset(request):
    if request.method == 'POST':
        post_args = copy(request.POST)
        form = PasswordResetForm(post_args)

        if form.is_valid():
            email = form.cleaned_data['email']
            account = UserAccount.objects.filter(email__exact=email).first()

            if account:
                site_domain = get_current_site(request).domain
                send_reset_password_mail_to_user(account, site_domain)
                return redirect('password-reset-done')
    else:
        form = PasswordResetForm()

    context = {'form': form}
    return render(request, 'teambuilding/account/password_reset.html', context)
