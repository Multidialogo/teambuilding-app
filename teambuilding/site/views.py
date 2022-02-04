from copy import copy
from datetime import date

from django import forms
from django.conf import settings
from django.contrib.auth import logout as logout_request, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext

from .forms import HappyBirthdayForm, RegistrationForm, UserForm
from .models import Notification, UserProfile
from .tasks import send_activation_mail_to_user, send_reset_password_mail_to_user


def home(request):
    context = {}
    return render(request, 'teambuilding/site/welcome.html', context)


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
            return render(request, 'teambuilding/site/auth/signup_success.html', context)
    else:
        form = RegistrationForm()

    context = {'signup_form': form}
    return render(request, 'teambuilding/site/auth/signup.html', context)


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
    return render(request, 'teambuilding/site/auth/activate.html', context)


def password_reset(request):
    if request.method == 'POST':
        post_args = copy(request.POST)
        form = PasswordResetForm(post_args)

        if form.is_valid():
            email = form.cleaned_data['email']
            account = get_user_model().objects.filter(email__exact=email).first()

            if account:
                site_domain = get_current_site(request).domain
                send_reset_password_mail_to_user(account, site_domain)
                return redirect('password-reset-done')
    else:
        form = PasswordResetForm()

    context = {'form': form}
    return render(request, 'teambuilding/site/auth/password_reset.html', context)


@login_required
def profile_detail(request):
    user_profile = request.user.profile
    context = {'user_profile': user_profile}
    return render(request, 'teambuilding/site/user/detail.html', context)


@login_required
def profile_update(request):
    user_profile = request.user.profile

    if request.method == 'POST':
        post_args = request.POST
        form = UserForm(post_args, instance=user_profile.account)

        if form.is_valid():
            with transaction.atomic():
                form.save()

            return redirect('user-profile')
    else:
        form = UserForm(instance=user_profile.account)

    context = {'user_form': form}
    return render(request, 'teambuilding/site/user/update.html', context)


@login_required
def notification_list(request):
    user_profile = request.user.profile
    notifications = Notification.objects.filter(user__pk=user_profile.pk)

    context = {'notifications': notifications}
    return render(request, 'teambuilding/site/notifications/list.html', context)


@login_required
def notification_detail(request, pk):
    notification = get_object_or_404(Notification, pk=pk)

    if request.user.profile != notification.recipient:
        raise PermissionDenied()

    if not notification.read:
        notification.read = True
        notification.save()

    context = {'notification': notification}
    return render(request, 'teambuilding/site/notifications/detail.html', context)


@login_required
def happy_birthday_send(request, bday_user_pk):
    birthday_user = get_object_or_404(UserProfile, pk=bday_user_pk)
    birthday_date = birthday_user.account.birth_date
    today = date.today()

    if today.day != birthday_date.day or today.month != birthday_date.month:
        raise PermissionDenied()

    if request.method == 'POST':
        post_args = copy(request.POST)
        post_args.update({
            'sender': request.user.profile,
            'recipient': birthday_user,
        })

        form = HappyBirthdayForm(post_args)

        if form.is_valid():
            with transaction.atomic():
                form.save()
                return redirect('home')
    else:
        form = HappyBirthdayForm()

    form.fields['sender'].widget = forms.HiddenInput()
    form.fields['recipient'].widget = forms.HiddenInput()

    context = {'happy_birthday_form': form}
    return render(request, 'teambuilding/site/user/wish_happy_bday.html', context)
