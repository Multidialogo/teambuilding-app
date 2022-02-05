from copy import copy
from datetime import date

from django import forms
from django.conf import settings
from django.contrib.auth import logout as logout_request, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import (
    LoginView as AuthLoginView, PasswordResetDoneView as AuthPasswordResetDoneView,
    PasswordResetConfirmView as AuthPasswordResetConfirmView,
    PasswordResetCompleteView as AuthPasswordResetCompleteView
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext

from .forms import HappyBirthdayForm, RegistrationForm, UserNicknameForm
from .models import Notification, UserProfile
from .tasks import send_user_activation_mail, send_reset_password_mail


def home(request):
    context = {}
    return render(request, 'teambuilding/site/welcome.html', context)


class LoginView(AuthLoginView):
    template_name = 'teambuilding/site/auth/login.html'


class PasswordResetDoneView(AuthPasswordResetDoneView):
    template_name = 'teambuilding/site/auth/password_reset_done.html'


class PasswordResetConfirmView(AuthPasswordResetConfirmView):
    template_name = 'teambuilding/site/auth/password_reset_confirm.html'


class PasswordResetCompleteView(AuthPasswordResetCompleteView):
    template_name = 'teambuilding/site/auth/password_reset_complete.html'


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
            try:
                site_domain = get_current_site(request).domain
                with transaction.atomic():
                    user = form.save()
                    # l'invio della mail avviene all'interno della transazione
                    # atomica, in modo che se ci sono problemi nell'invio della
                    # mail, quindi l'utente non puo' registrarsi, il record
                    # non viene inserito nel database
                    send_user_activation_mail(user, site_domain)
            except (Exception,) as e:
                form.add_error(None, str(e))

            if not form.errors:
                context = {'registered_user': user}
                return render(request, 'teambuilding/site/auth/signup_success.html', context)
    else:
        form = RegistrationForm()

    context = {'signup_form': form}
    return render(request, 'teambuilding/site/auth/signup.html', context)


def activate_user(request, uidb64, token):
    try:
        user_id = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=user_id)
    except(TypeError, ValueError, OverflowError, settings.AUTH_USER_MODEL.DoesNotExist):
        user = None

    if user and not user.is_active:
        try:
            token_check = default_token_generator.check_token(user, token)
            if token_check:
                with transaction.atomic():
                    user.is_active = True
                    user.save()
        except (Exception,):
            user.is_active = False

    if user and user.is_active:
        message = gettext("Your account has been activated.")
    else:
        message = gettext("Invalid link.")

    context = {'message': message}
    return render(request, 'teambuilding/site/auth/activate.html', context)


def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            site_domain = get_current_site(request).domain

            send_reset_password_mail(email, site_domain)
            return redirect('password-reset-done')
    else:
        form = PasswordResetForm()

    context = {'form': form}
    return render(request, 'teambuilding/site/auth/password_reset.html', context)


@login_required
def profile_detail(request, pk=None):
    if not pk:
        pk = request.user.profile.pk
        return redirect('user-profile', pk=pk)

    user_profile = get_object_or_404(UserProfile, pk=pk)
    context = {'user_profile': user_profile}
    return render(request, 'teambuilding/site/user/detail.html', context)


@login_required
def profile_update(request, pk=None):
    if not pk:
        pk = request.user.profile.pk
        return redirect('user-profile-update', pk=pk)

    user_profile = get_object_or_404(UserProfile, pk=pk)

    if request.user != user_profile.account:
        raise PermissionDenied()

    if request.method == 'POST':
        form = UserNicknameForm(request.POST, instance=user_profile.account)

        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
            except (Exception,) as e:
                form.add_error(None, str(e))

            if not form.errors:
                return redirect('user-profile')
    else:
        form = UserNicknameForm(instance=user_profile.account)

    context = {'user_form': form}
    return render(request, 'teambuilding/site/user/update.html', context)


@login_required
def notification_list(request, user_pk=None):
    if not user_pk:
        user_pk = request.user.pk
        return redirect('user-profile-update', pk=user_pk)

    user = get_object_or_404(get_user_model(), pk=user_pk)

    if request.user != user:
        raise PermissionDenied()

    notifications = Notification.objects.filter(user__pk=user_pk)
    context = {'notifications': notifications}
    return render(request, 'teambuilding/site/notifications/list.html', context)


@login_required
def notification_detail(request, pk, user_pk=None):
    if not user_pk:
        user_pk = request.user.pk
        return redirect('user-profile-update', pk=user_pk)

    user = get_object_or_404(get_user_model(), pk=user_pk)

    if request.user != user:
        raise PermissionDenied()

    notification = get_object_or_404(Notification, pk=pk)

    if user != notification.recipient:
        raise PermissionDenied()

    if not notification.read:
        notification.read = True
        notification.save()

    context = {'notification': notification}
    return render(request, 'teambuilding/site/notifications/detail.html', context)


@login_required
def happy_birthday_send(request, pk):
    birthday_user = get_object_or_404(get_user_model(), pk=pk)
    birthday_date = birthday_user.birth_date
    today = date.today()

    if today.day != birthday_date.day or today.month != birthday_date.month:
        raise PermissionDenied()

    if request.method == 'POST':
        post_args = copy(request.POST)
        post_args.update({
            'sender': request.user,
            'recipient': birthday_user,
        })

        form = HappyBirthdayForm(post_args)

        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
            except (Exception,) as e:
                form.add_error(None, str(e))

            if not form.errors:
                return redirect('home')
    else:
        form = HappyBirthdayForm()

    form.fields['sender'].widget = forms.HiddenInput()
    form.fields['recipient'].widget = forms.HiddenInput()

    context = {'happy_birthday_form': form}
    return render(request, 'teambuilding/site/user/wish_happy_bday.html', context)
