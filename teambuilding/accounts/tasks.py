from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext


def send_activation_mail_to_user(user, site_domain):
    if not user.is_superuser:
        base64_user_id = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_path = reverse('activate', kwargs={'uid_64': base64_user_id, 'token': token})
        activation_link = "https://%s%s" % (site_domain, activation_path)
        message = gettext(
            "Hi %(nickname)s,\n"
            "Please click on the link to confirm your registration, %(link)s\n"
            "If you think it's not you, then just ignore this email."
        ) % (
            {'nickname': user.nickname, 'link': activation_link}
        )

        mail_subject = gettext('Taste & Purchase account activation')
        email = EmailMessage(mail_subject, message, to=(user.email,))
        email.send()
