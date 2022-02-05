import calendar
from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext

from .models import UserProfile, Notification, HappyBirthdayMessage


def send_user_activation_mail(user, site_domain):
    if user.is_superuser:
        return

    base64_user_id = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    activation_url_args = {'uidb64': base64_user_id, 'token': token}
    activation_url_path = reverse('user-account-activate', kwargs=activation_url_args)
    activation_link = "https://%s%s" % (site_domain, activation_url_path)

    mail_subject = gettext('Teambuilding Platform account activation')
    mail_message = gettext(
        "Hi %(nickname)s,\n"
        "Please click on the link to confirm your registration, %(link)s\n"
        "If you think it's not you, then just ignore this email."
    ) % ({
        'nickname': user.nickname,
        'link': activation_link
    })

    email_message = EmailMessage(
        mail_subject,
        mail_message,
        to=[user.email]
    )
    email_message.send()


def send_reset_password_mail(email, site_domain):
    user = get_user_model().objects.filter(email=email).first()

    if not user:
        return

    base64_user_id = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

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
        "The Teambuilding Platform Team\n"
    ) % ({
        'nickname': user.nickname,
        'reset-link': reset_link,
        'website-link': website_link
    })

    email = EmailMessage(mail_subject, message, to=(email,))
    email.send()


def create_user_profile(user_account):
    UserProfile.objects.create(account=user_account)


def check_users_birthday():
    today = date.today()
    today_year_days = (today - date(today.year, 1, 1)).days

    users = get_user_model().objects.all()

    for user in users:
        birth_date = user.birth_date
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
    body = gettext("Happy birthday, %s!") % birthday_user.nickname

    HappyBirthdayMessage.objects.create(
        recipient=birthday_user,
        message=body
    )


def notify_users_about_today_birthday(birthday_user):
    users_to_notify = get_user_model().objects.exclude(email=birthday_user.email)
    subject = gettext("Today is %s's birthday!") % birthday_user.nickname

    link_kwargs = {'pk': birthday_user.pk}
    body = gettext(
        "Today is %(user)s's birthday! Wish happy birthday with the following link: " 
        "%(link)s"
    ) % {
        'user': birthday_user.nickname,
        'link': reverse('user-happy-bday', kwargs=link_kwargs)
    }

    for user_to_notify in users_to_notify:
        Notification.objects.create(
            recipient=user_to_notify,
            subject=subject,
            body=body,
            send_email=True
        )


def notify_users_about_incoming_birthday(birthday_user, in_days):
    users_to_notify = get_user_model().objects.exclude(email=birthday_user.email)
    subject = gettext("Incoming birthday alert!")
    body = gettext("%(user)s birthday is in %(in_days)01.0f") % {
        'user': birthday_user.nickname,
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
        notification.subject,
        notification.body,
        to=[notification.recipient.email, ]
    )
    email.send()