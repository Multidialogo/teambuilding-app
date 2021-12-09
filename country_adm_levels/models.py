from django.db import models


class Country(models.Model):
    country_code = models.CharField('Code', max_length=2, primary_key=True)

    class Meta:
        ordering = ['country_code']

    def __str__(self):
        return self.country_code


class CountryAdminLevelMapping(models.Model):
    country_code = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Country')
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
        ordering = ['country_code']

    def __str__(self):
        return self.country_code
