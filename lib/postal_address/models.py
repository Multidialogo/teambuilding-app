from django.db import models

from .validators import validate_zip_code


class Country(models.Model):
    country_code = models.CharField('Code', max_length=2, primary_key=True)

    class Meta:
        ordering = ['country_code']
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.country_code


class CountryAdminLevelMapping(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    administrative_level_1_mandatory = models.BooleanField('Adm. Lvl. 1 Mandatory')
    administrative_level_1_endonym = models.CharField('Adm. Lvl. 1 Endonym', max_length=50, blank=True, null=True)
    administrative_level_2_mandatory = models.BooleanField('Adm. Lvl. 2 Mandatory')
    administrative_level_2_endonym = models.CharField('Adm. Lvl. 2 Endonym', max_length=50, blank=True, null=True)
    administrative_level_3_mandatory = models.BooleanField('Adm. Lvl. 3 Mandatory')
    administrative_level_3_endonym = models.CharField('Adm. Lvl. 3 Endonym', max_length=50, blank=True, null=True)
    administrative_level_4_mandatory = models.BooleanField('Adm. Lvl. 4 Mandatory')
    administrative_level_4_endonym = models.CharField('Adm. Lvl. 4 Endonym', max_length=50, blank=True, null=True)
    administrative_level_5_mandatory = models.BooleanField('Adm. Lvl. 5 Mandatory')
    administrative_level_5_endonym = models.CharField('Adm. Lvl. 5 Endonym', max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['country']

    def __str__(self):
        return self.country


class PostalAddress(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    zip_code = models.CharField('Zip code', max_length=5, validators=[validate_zip_code])
    street = models.CharField('Street', max_length=100)
    adm_level_1 = models.CharField('Administrative Level 1', max_length=100, blank=True)
    adm_level_2 = models.CharField('Administrative Level 2', max_length=100, blank=True)
    adm_level_3 = models.CharField('Administrative Level 3', max_length=100, blank=True)
    adm_level_4 = models.CharField('Administrative Level 4', max_length=100, blank=True)
    adm_level_5 = models.CharField('Administrative Level 5', max_length=100, blank=True)

    def __str__(self):
        return "%s, %s, %s, %s" % (self.adm_level_3, self.street, self.zip_code, self.country)
