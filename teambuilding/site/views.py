from copy import copy
from datetime import date

from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.translation import gettext

from teambuilding.accounts.forms import UserAccountForm

from .forms import UserProfileForm, HappyBirthdayForm
from .models import Notification, User


def home(request):
    context = {}
    return render(request, 'teambuilding/site/welcome.html', context)


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
        form = UserAccountForm(post_args, instance=user_profile.account)
        form_extra = UserProfileForm(post_args, instance=user_profile)

        if form.is_valid() and form_extra.is_valid():
            with transaction.atomic():
                form.save()
                form_extra.save()

            return redirect('user-profile')
    else:
        form = UserAccountForm(instance=user_profile.account)
        form_extra = UserProfileForm(instance=user_profile)

    context = {'user_form': form, 'user_extra_form': form_extra}
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

    if request.user.profile != notification.user:
        raise PermissionDenied()

    if not notification.read:
        notification.read = True
        notification.save()

    context = {'notification': notification}
    return render(request, 'teambuilding/site/notifications/detail.html', context)


@login_required
def happy_birthday_send(request, bday_user_pk):
    birthday_user = get_object_or_404(User, pk=bday_user_pk)
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
