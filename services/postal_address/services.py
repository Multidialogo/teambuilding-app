from services.postal_address.models import Country


def is_country_code_valid(country_code):
    is_valid = Country.objects.filter(country_code=country_code).exists()
    return is_valid


def safe_country_code(country_code, fallback_value='IT'):
    if is_country_code_valid(country_code):
        return country_code
    return fallback_value
