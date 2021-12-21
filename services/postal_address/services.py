from services.postal_address.models import Country


def safe_country_code(country_code, fallback_value='IT'):
    if Country.objects.filter(country_code).exists():
        return country_code
    return fallback_value
