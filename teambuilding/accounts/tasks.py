from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext


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
