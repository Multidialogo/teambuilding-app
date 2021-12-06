from django import forms

from products.models import Producer


class AddProducerForm(forms.ModelForm):

    class Meta:
        model = Producer
        fields = ('name', 'email', 'phone', 'address_country', 'address_zip_code', 'address_street',
                  'address_adm_level_1', 'address_adm_level_2', 'address_adm_level_3', 'address_adm_level_4',
                  'address_adm_level_5')
