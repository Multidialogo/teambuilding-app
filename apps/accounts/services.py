from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def send_activation_mail_to_user(user, domain):
    mail_subject = 'Activate your Taste & Purchase account.'
    message = render_to_string(
        'registration/activate_email.html', {
            'user': user,
            'domain': domain,
            'user_id': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        }
    )
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", '')
    user.email_user(mail_subject, message, from_email)
