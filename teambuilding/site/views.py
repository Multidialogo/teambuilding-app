from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404
from django.shortcuts import redirect, render

from teambuilding.accounts.forms import UserAccountForm

from .forms import UserProfileForm


def home(request):
    context = {}
    return render(request, 'teambuilding/site/welcome.html', context)


@login_required
def profile_detail(request):
    user_profile = request.user.profile

    if not user_profile:
        raise Http404()

    context = {'user_profile': user_profile}
    return render(request, 'teambuilding/site/user/detail.html', context)


@login_required
def profile_update(request):
    user_profile = request.user.profile

    if not user_profile:
        raise Http404()

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
