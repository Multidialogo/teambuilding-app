import calendar
from datetime import date

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext

from .models import UserProfile, Notification, HappyBirthdayMessage


def send_activation_mail_to_user(account, site_domain):
    if not account.is_superuser:
        base64_user_id = urlsafe_base64_encode(force_bytes(account.pk))
        token = default_token_generator.make_token(account)

        activation_url_args = {'uidb64': base64_user_id, 'token': token}
        activation_url_path = reverse('activate', kwargs=activation_url_args)
        activation_link = "https://%s%s" % (site_domain, activation_url_path)

        mail_subject = gettext('Taste & Purchase account activation')
        message = gettext(
            "Hi %(nickname)s,\n"
            "Please click on the link to confirm your registration, %(link)s\n"
            "If you think it's not you, then just ignore this email."
        ) % ({
            'nickname': account.nickname,
            'link': activation_link
        })

        email = EmailMessage(mail_subject, message, to=(account.email,))
        email.send()


def send_reset_password_mail_to_user(account, site_domain):
    base64_user_id = urlsafe_base64_encode(force_bytes(account.pk))
    token = default_token_generator.make_token(account)

    reset_url_args = {'uidb64': base64_user_id, 'token': token}
    reset_url_path = reverse('password-reset-confirm', kwargs=reset_url_args)
    reset_link = "https://%s%s" % (site_domain, reset_url_path)
    website_link = reverse('home')

    mail_subject = gettext('Password Reset Requested')
    message = gettext(
        "Hello,\n"
        "We've received a request to reset the password for your account for this email address.\n"
        "To initiate the password reset process for your account, click the link below.\n"
        "\n"
        "%(reset-link)s\n"
        "This link can only be used once. If you need to reset your password again,\n"
        "please visit %(website-link)s and request another reset.\n"
        "\n"
        "If you did not make this request, you can simply ignore this email.\n"
        "\n"
        "Sincerely,\n"
        "The Taste & Purchase Team\n"
    ) % ({
        'nickname': account.nickname,
        'reset-link': reset_link,
        'website-link': website_link
    })

    email = EmailMessage(mail_subject, message, to=(account.email,))
    email.send()


def create_user_profile(user_account):
    UserProfile.objects.create(account=user_account)


def check_users_birthday():
    today = date.today()
    today_year_days = (today - date(today.year, 1, 1)).days

    users = UserProfile.objects.all()

    for user in users:
        birth_date = user.account.birth_date
        birth_date_year_days = (birth_date - date(birth_date.year, 1, 1)).days

        if birth_date_year_days < today_year_days:
            birth_date_year_days += 365 + calendar.isleap(today.year)

        in_days = birth_date_year_days - today_year_days

        if in_days == 0:
            send_happy_birthday_to_user(user)
            notify_users_about_today_birthday(user)
        elif in_days in [1, 7]:
            notify_users_about_incoming_birthday(user, in_days)


def send_happy_birthday_to_user(birthday_user):
    body = gettext("Happy birthday, %s!") % birthday_user.account.nickname

    HappyBirthdayMessage.objects.create(
        recipient=birthday_user,
        message=body
    )


def notify_users_about_today_birthday(birthday_user):
    users_to_notify = UserProfile.objects.exclude(account__email=birthday_user.account.email)
    subject = gettext("Today is %s's birthday!") % birthday_user.account.nickname

    link_kwargs = {'bday_user_pk': birthday_user.pk}
    body = gettext(
        "Today is %(user)s's birthday! Wish happy birthday with the following link: " 
        "%(link)s"
    ) % {
        'user': birthday_user.account.nickname,
        'link': reverse('user-profile-happy-bday', kwargs=link_kwargs)
    }

    for user_to_notify in users_to_notify:
        Notification.objects.create(
            recipient=user_to_notify,
            subject=subject,
            body=body,
            send_email=True
        )


def notify_users_about_incoming_birthday(birthday_user, in_days):
    users_to_notify = UserProfile.objects.exclude(account__email=birthday_user.account.email)
    subject = gettext("Incoming birthday alert!")
    body = gettext("%(user)s birthday is in %(in_days)01.0f") % {
        'user': birthday_user.account.nickname,
        'in_days': in_days
    }

    for user_to_notify in users_to_notify:
        Notification.objects.create(
            recipient=user_to_notify,
            subject=subject,
            body=body,
            send_email=False
        )


def send_email_from_notification(notification):
    email = EmailMessage(
        notification.subject, notification.body, to=[notification.recipient.account.email, ]
    )
    email.send()
