from django.core.exceptions import ValidationError


def validate_zip_code(value):
    str_value = str(value)
    if not str_value.isdigit():
        raise ValidationError(
            '%(value)s is not a valid zip code',
            params={'value': value},
        )
