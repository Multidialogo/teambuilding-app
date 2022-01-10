from django.db import models
from django.utils.translation import gettext_lazy as _, gettext

from .validators import validate_zip_code


class Country(models.Model):
    country_code = models.CharField(_('country code'), max_length=2, primary_key=True)

    class Meta:
        ordering = ['country_code']
        verbose_name = _("country")
        verbose_name_plural = _("countries")

    def __str__(self):
        return self.country_code


class CountryAdminLevelMapping(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    administrative_level_1_mandatory = models.BooleanField('adm. Lvl. 1 mandatory')
    administrative_level_1_endonym = models.CharField('adm. Lvl. 1 endonym', max_length=50, blank=True, null=True)
    administrative_level_2_mandatory = models.BooleanField('adm. Lvl. 2 mandatory')
    administrative_level_2_endonym = models.CharField('adm. Lvl. 2 endonym', max_length=50, blank=True, null=True)
    administrative_level_3_mandatory = models.BooleanField('adm. Lvl. 3 mandatory')
    administrative_level_3_endonym = models.CharField('adm. Lvl. 3 endonym', max_length=50, blank=True, null=True)
    administrative_level_4_mandatory = models.BooleanField('adm. Lvl. 4 mandatory')
    administrative_level_4_endonym = models.CharField('adm. Lvl. 4 endonym', max_length=50, blank=True, null=True)
    administrative_level_5_mandatory = models.BooleanField('adm. Lvl. 5 mandatory')
    administrative_level_5_endonym = models.CharField('adm. Lvl. 5 endonym', max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['country']

    def __str__(self):
        return self.country


class PostalAddress(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_("country"))
    zip_code = models.CharField(_("zip code"), max_length=5, validators=[validate_zip_code])
    street = models.CharField(_("street"), max_length=100)
    adm_level_1 = models.CharField(_("administrative level 1"), max_length=100, blank=True)
    adm_level_2 = models.CharField(_("administrative level 2"), max_length=100, blank=True)
    adm_level_3 = models.CharField(_("administrative level 3"), max_length=100, blank=True)
    adm_level_4 = models.CharField(_("administrative level 4"), max_length=100, blank=True)
    adm_level_5 = models.CharField(_("administrative level 5"), max_length=100, blank=True)

    class Meta:
        verbose_name = _("postal address")
        verbose_name_plural = _("postal addresses")

    def __str__(self):
        return gettext(
            "%(street)s, %(adm-3)s, %(adm-1)s, %(zipcode)s, %(country)s"
            "%(adm-2)0s%(adm-4)0s%(adm-5)0s") % {
                'country': str(self.country),
                'zipcode': self.zip_code,
                'street': self.street,
                'adm-1': self.adm_level_1,
                'adm-2': self.adm_level_2,
                'adm-3': self.adm_level_3,
                'adm-4': self.adm_level_4,
                'adm-5': self.adm_level_5
            }
