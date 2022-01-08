from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.users.forms import UserForm


@login_required
def profile_detail(request):
    context = {'user': request.user}
    return render(request, 'account/detail.html', context)


@login_required
def profile_update(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('user-profile')
    else:
        form = UserForm(instance=request.user)

    context = {'user_form': form}
    return render(request, 'account/update.html', context)
