import phonenumbers

from django.utils.translation import gettext

from phonenumber_field.formfields import PhoneNumberField as BasePhoneNumberField
from phonenumber_field.phonenumber import to_python


# NOTA: questa classe esiste perche' le traduzioni del messaggio di errore 'invalido'
# della classe del componente base non funzionano correttamente
class PhoneNumberField(BasePhoneNumberField):
    def __init__(self, *args, region=None, **kwargs):
        has_invalid_message = hasattr(self, 'error_messages') and 'invalid' in self.error_messages
        super().__init__(*args, **kwargs)

        if not has_invalid_message:
            if region:
                number = phonenumbers.example_number(region)
                example_number = to_python(number).as_national
                # Translators: %(example-number)s is a national phone number.
                error_message = gettext(
                    "Enter a valid phone number (e.g. %(example-number)s) "
                    "or a number with an international call prefix."
                ) % (
                                    {'example-number': example_number}
                                )
            else:
                example_number = "+12125552368"
                # Translators: %(example-number)s is a national phone number.
                error_message = gettext("Enter a valid phone number (e.g. %(example-number)s).") % (
                    {'example-number': example_number}
                )

            self.error_messages["invalid"] = error_message
