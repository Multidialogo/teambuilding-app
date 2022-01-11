from phonenumber_field.modelfields import PhoneNumberField as BasePhoneNumberField

from . import formfields


class PhoneNumberField(BasePhoneNumberField):
    def formfield(self, **kwargs):
        defaults = {
            "form_class": formfields.PhoneNumberField,
            "region": self.region,
            "error_messages": self.error_messages,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
