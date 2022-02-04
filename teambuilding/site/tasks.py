import calendar
from datetime import date

from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.translation import gettext

from .models import User, Notification, HappyBirthdayMessage


def create_user_profile(user_account):
    User.objects.create(account=user_account)


def check_users_birthday():
    today = date.today()
    today_year_days = (today - date(today.year, 1, 1)).days

    users = User.objects.all()

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
    users_to_notify = User.objects.exclude(account__email=birthday_user.account.email)
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
    users_to_notify = User.objects.exclude(account__email=birthday_user.account.email)
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
