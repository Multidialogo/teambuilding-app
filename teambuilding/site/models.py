from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _, gettext


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, birth_date, **extra_fields):
        if not email:
            raise ValueError(gettext("The Email must be set"))
        if not password:
            raise ValueError(gettext("The Password must be set"))
        if not birth_date:
            raise ValueError(gettext("The Birth Date must be set"))

        email = self.normalize_email(email)
        user = self.model(email=email, birth_date=birth_date, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password, birth_date, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)

        return self._create_user(email, password, birth_date, **extra_fields)

    def create_superuser(self, email, password, birth_date, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, birth_date, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(
        verbose_name=_('email address'),
        blank=False,
        unique=True)
    nickname = models.CharField(
        max_length=100,
        verbose_name=_('nickname'),
        unique=True)
    birth_date = models.DateField(
        _("birth date"),
        help_text=_("Format: dd/mm/YYYY"))

    username = None
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['birth_date']

    def __str__(self):
        return self.nickname

    def save(self, *args, **kwargs):
        if (not self.nickname) or self.nickname.isspace():
            self.nickname = self.email

        super().save(*args, **kwargs)

    def clean(self):
        super().clean()

        if (not self.nickname) or self.nickname.isspace():
            self.nickname = self.email


class UserProfile(models.Model):
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_("account"))

    class Meta:
        ordering = ['account__nickname']
        verbose_name = _("user profile")
        verbose_name_plural = _("user profiles")

    def __str__(self):
        return str(self.account)


class HappyBirthdayMessage(models.Model):
    created_at = models.DateField(auto_now_add=True)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("sender"),
        related_name="+",
        null=True)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("recipient"),
        related_name="+")
    message = models.TextField(
        _("body"),
        max_length=500)

    class Meta:
        unique_together = ['created_at', 'recipient', 'sender']
        ordering = ['created_at', 'recipient', 'sender']
        verbose_name = _("happy birthday message")
        verbose_name_plural = _("happy birthday messages")

    def __str__(self):
        return gettext("Happy birthday message from %(sender)s to %(recipient)s") % (
            {'sender': str(self.sender), 'recipient': str(self.recipient)}
        )


class Notification(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("recipient"))
    subject = models.CharField(
        _("subject"),
        max_length=80)
    body = models.TextField(
        _("body"),
        max_length=256)
    read = models.BooleanField(
        _("read"),
        default=False)

    class Meta:
        ordering = ['created_at']
        verbose_name = _("notification")
        verbose_name_plural = _("notifications")

    def __str__(self):
        return self.subject


class Event(models.Model):
    start_date = models.DateTimeField(
        _("event start"),
        help_text=_("Format: dd/mm/YYYY hh:mm"))
    end_date = models.DateTimeField(
        _("event end"),
        help_text=_("Format: dd/mm/YYYY hh:mm"))
    title = models.CharField(
        _("title"),
        max_length=50)
    description = models.CharField(
        _("description"),
        max_length=100)

    class Meta:
        ordering = ['start_date', 'title']
        verbose_name = _("event")
        verbose_name_plural = _("events")

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.start_date > self.end_date:
            raise ValidationError({
                'start_date': gettext("End date must come after start date."),
                'end_date': gettext("End date must come after start date.")
            })
