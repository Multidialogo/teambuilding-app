from django.contrib.sites.shortcuts import get_current_site

from apps.accounts.services import send_activation_mail_to_user


def on_account_created(request, user):
    domain = get_current_site(request).domain
    send_activation_mail_to_user(user, domain)
