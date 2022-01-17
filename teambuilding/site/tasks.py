from .models import User


def create_user_profile(user_account):
    User.objects.create(account=user_account)
