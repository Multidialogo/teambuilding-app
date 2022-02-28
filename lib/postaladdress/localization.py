from .models import Country, CountryAdminLevelMapping
from .utils import safe_country_code


def setup_form_field(form, field_name, value, required):
    if value:
        form.fields[field_name].label = value
        form.fields[field_name].required = required
    else:
        form.fields.pop(field_name)


def localize_form(country_code, form):
    country_code = safe_country_code(country_code)
    country = Country.objects.get(pk=country_code)
    country_map = CountryAdminLevelMapping.objects.filter(country=country).first()

    form.initial['country'] = country
    form.fields['country'].empty_label = None

    setup_form_field(
        form,
        'adm_level_1',
        country_map.administrative_level_1_endonym,
        country_map.administrative_level_1_mandatory
    )

    setup_form_field(
        form,
        'adm_level_2',
        country_map.administrative_level_2_endonym,
        country_map.administrative_level_2_mandatory
    )

    setup_form_field(
        form,
        'adm_level_3',
        country_map.administrative_level_3_endonym,
        country_map.administrative_level_3_mandatory
    )

    setup_form_field(
        form,
        'adm_level_4',
        country_map.administrative_level_4_endonym,
        country_map.administrative_level_4_mandatory
    )

    setup_form_field(
        form,
        'adm_level_5',
        country_map.administrative_level_5_endonym,
        country_map.administrative_level_5_mandatory
    )

    return form


def localize_formset(country_code, formset):
    for form in formset:
        localize_form(country_code, form)

    return formset
