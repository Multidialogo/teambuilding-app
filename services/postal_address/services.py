from django.http import Http404

from services.postal_address.models import Country


def is_country_code_valid(country_code):
    is_valid = Country.objects.filter(country_code=country_code).exists()
    return is_valid


def safe_country_code(country_code, fallback_value='IT'):
    if not is_country_code_valid(country_code):
        if not is_country_code_valid(fallback_value):
            if not Country.objects.exists():
                raise Http404()
            else:
                country_code = Country.objects.values('country_code').first()
        else:
            country_code = fallback_value
    return country_code
