from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        if not password:
            raise ValueError('The Password must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):

    email = models.EmailField(max_length=100, unique=True)
    nickname = models.CharField(max_length=100)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname = self.email
        super(User, self).save(*args, **kwargs)

    def get_email(self):
        return self.email

    def get_nickname(self):
        return self.nickname

    def get_is_active(self):
        return self.is_active

    def get_is_staff(self):
        return self.is_staff
