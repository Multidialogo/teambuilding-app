from datetime import timedelta, date

from django.contrib.auth import get_user_model

from .models import User
from .signals import birthday_found


def create_user_profile(user_account):
    User.objects.create(account=user_account)


def check_users_birthday():
    today = date.today()
    seven_days_ago = today - timedelta(days=7)
    birthday_users = get_user_model().objects.filter(birth_date__range=[seven_days_ago, today])

    for user in birthday_users:
        in_days = (user.birth_date - today).days
        birthday_found.send(sender=check_users_birthday, user=user, in_days=in_days)
