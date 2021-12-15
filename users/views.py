from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from users.forms import RegisterForm, ChangeNicknameForm
from users.models import User


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            # TODO : possibile refactoring
            current_site = get_current_site(request)
            mail_subject = 'Activate your Taste & Purchase account.'
            message = render_to_string(
                'acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                }
            )
            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", '')
            to_email = form.cleaned_data.get('email')
            send_mail(
                mail_subject,
                message,
                from_email,
                [to_email],
                fail_silently=False,
            )

            return HttpResponse(
                'Please confirm your email address '
                'to complete the registration'
            )
    else:
        form = RegisterForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def change_nickname(request):
    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('profile')
    else:
        form = ChangeNicknameForm()
    return render(request, 'change_nickname.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    return render(request, 'profile.html', {})
