from django.db import models

from .validators import validate_zip_code


class Country(models.Model):
    country_code = models.CharField('codice nazione', max_length=2, primary_key=True)

    class Meta:
        ordering = ['country_code']
        verbose_name = 'nazione'
        verbose_name_plural = 'nazioni'

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
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='nazione')
    zip_code = models.CharField('codice postale', max_length=5, validators=[validate_zip_code])
    street = models.CharField('strada', max_length=100)
    adm_level_1 = models.CharField('livello amministrativo 1', max_length=100, blank=True)
    adm_level_2 = models.CharField('livello amministrativo 2', max_length=100, blank=True)
    adm_level_3 = models.CharField('livello amministrativo 3', max_length=100, blank=True)
    adm_level_4 = models.CharField('livello amministrativo 4', max_length=100, blank=True)
    adm_level_5 = models.CharField('livello amministrativo 5', max_length=100, blank=True)

    class Meta:
        verbose_name = 'indirizzo postale'
        verbose_name_plural = 'indirizzi postali'

    def __str__(self):
        return "%s, %s, %s, %s" % (self.adm_level_3, self.street, self.zip_code, self.country)
