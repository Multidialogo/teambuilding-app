from django.db import migrations
from django.utils.translation import gettext


def insert_data(apps, schema_editor):
    Country = apps.get_model('postaladdress', 'Country')
    CountryAdminLevelMapping = apps.get_model('postaladdress', 'CountryAdminLevelMapping')

    country_it = Country(country_code='IT')
    country_it.save()

    map_it = CountryAdminLevelMapping(
        country=country_it,
        administrative_level_1_mandatory=False,
        administrative_level_1_endonym=gettext("Regione"),
        administrative_level_2_mandatory=True,
        administrative_level_2_endonym=gettext("Provincia"),
        administrative_level_3_mandatory=True,
        administrative_level_3_endonym=gettext("Comune"),
        administrative_level_4_mandatory=False,
        administrative_level_4_endonym=gettext("Frazione"),
        administrative_level_5_mandatory=False,
        administrative_level_5_endonym=None,
    )
    map_it.save()

    country_fr = Country(country_code='FR')
    country_fr.save()

    map_fr = CountryAdminLevelMapping(
        country=country_fr,
        administrative_level_1_mandatory=False,
        administrative_level_1_endonym=gettext("Région"),
        administrative_level_2_mandatory=False,
        administrative_level_2_endonym=gettext("Département"),
        administrative_level_3_mandatory=True,
        administrative_level_3_endonym=gettext("Arrondissement"),
        administrative_level_4_mandatory=False,
        administrative_level_4_endonym=gettext("Canton"),
        administrative_level_5_mandatory=False,
        administrative_level_5_endonym=gettext("Intercommunality"),
    )
    map_fr.save()

    country_es = Country(country_code='ES')
    country_es.save()

    map_es = CountryAdminLevelMapping(
        country=country_es,
        administrative_level_1_mandatory=False,
        administrative_level_1_endonym=gettext("Comunidad Autónomas"),
        administrative_level_2_mandatory=False,
        administrative_level_2_endonym=gettext("Provincia"),
        administrative_level_3_mandatory=False,
        administrative_level_3_endonym=gettext("Comarca"),
        administrative_level_4_mandatory=True,
        administrative_level_4_endonym=gettext("Municipio"),
        administrative_level_5_mandatory=False,
        administrative_level_5_endonym=None,
    )
    map_es.save()

    country_pt = Country(country_code='PT')
    country_pt.save()

    map_pt = CountryAdminLevelMapping(
        country=country_pt,
        administrative_level_1_mandatory=False,
        administrative_level_1_endonym=gettext("Distrito"),
        administrative_level_2_mandatory=True,
        administrative_level_2_endonym=gettext("Concelho"),
        administrative_level_3_mandatory=False,
        administrative_level_3_endonym=gettext("Freguesia"),
        administrative_level_4_mandatory=False,
        administrative_level_4_endonym=None,
        administrative_level_5_mandatory=False,
        administrative_level_5_endonym=None,
    )
    map_pt.save()

    country_ch = Country(country_code='CH')
    country_ch.save()

    map_ch = CountryAdminLevelMapping(
        country=country_ch,
        administrative_level_1_mandatory=False,
        administrative_level_1_endonym=gettext("Canton"),
        administrative_level_2_mandatory=False,
        administrative_level_2_endonym=gettext("District"),
        administrative_level_3_mandatory=True,
        administrative_level_3_endonym=gettext("Commune"),
        administrative_level_4_mandatory=False,
        administrative_level_4_endonym=None,
        administrative_level_5_mandatory=False,
        administrative_level_5_endonym=None,
    )
    map_ch.save()

    country_ro = Country(country_code='RO')
    country_ro.save()

    map_ro = CountryAdminLevelMapping(
        country=country_ro,
        administrative_level_1_mandatory=False,
        administrative_level_1_endonym=gettext("Județ"),
        administrative_level_2_mandatory=True,
        administrative_level_2_endonym=gettext("Orașe"),
        administrative_level_3_mandatory=False,
        administrative_level_3_endonym=None,
        administrative_level_4_mandatory=False,
        administrative_level_4_endonym=None,
        administrative_level_5_mandatory=False,
        administrative_level_5_endonym=None,
    )
    map_ro.save()

    country_za = Country(country_code='ZA')
    country_za.save()

    map_za = CountryAdminLevelMapping(
        country=country_za,
        administrative_level_1_mandatory=False,
        administrative_level_1_endonym=gettext("Province"),
        administrative_level_2_mandatory=False,
        administrative_level_2_endonym=gettext("District municipality"),
        administrative_level_3_mandatory=True,
        administrative_level_3_endonym=gettext("Local municipality"),
        administrative_level_4_mandatory=False,
        administrative_level_4_endonym=gettext("Ward"),
        administrative_level_5_mandatory=False,
        administrative_level_5_endonym=None,
    )
    map_za.save()

    country_jp = Country(country_code='JP')
    country_jp.save()

    map_jp = CountryAdminLevelMapping(
        country=country_jp,
        administrative_level_1_mandatory=False,
        administrative_level_1_endonym=gettext("Todōfuken"),
        administrative_level_2_mandatory=True,
        administrative_level_2_endonym=gettext("Shi"),
        administrative_level_3_mandatory=False,
        administrative_level_3_endonym=gettext("Shichōsonku"),
        administrative_level_4_mandatory=False,
        administrative_level_4_endonym=None,
        administrative_level_5_mandatory=False,
        administrative_level_5_endonym=None,
    )
    map_jp.save()


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('postaladdress', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_data),
    ]
