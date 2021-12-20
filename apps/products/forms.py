from django import forms

from services.country_adm_levels.models import Country, CountryAdminLevelMapping

from .models import Producer, Product, ProductPurchaseOption


class ProductPurchaseOptionForm(forms.ModelForm):

    class Meta:
        model = ProductPurchaseOption
        fields = ('product', 'quantity', 'priceInCents')

    def __init__(self, *args, **kwargs):
        if 'product' in kwargs:
            product_in = kwargs.pop('product')
            super(ProductPurchaseOptionForm, self).__init__(*args, **kwargs)
            self.fields['product'].initial = product_in
        else:
            super(ProductPurchaseOptionForm, self).__init__(*args, **kwargs)


class AddProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('title', 'description', 'producer')


class AddProducerForm(forms.ModelForm):

    class Meta:
        model = Producer
        fields = ('name', 'email', 'phone', 'address_country', 'address_zip_code', 'address_street',
                  'address_adm_level_1', 'address_adm_level_2', 'address_adm_level_3', 'address_adm_level_4',
                  'address_adm_level_5')

    def __init__(self, *args, **kwargs):
        country_code_in = kwargs.pop('country')
        super(AddProducerForm, self).__init__(*args, **kwargs)

        address_country_in = Country.objects.filter(country_code=country_code_in).first()
        country_map = CountryAdminLevelMapping.objects.filter(country_code=address_country_in).first()
        self.fields['address_country'].initial = address_country_in
        self.fields['address_country'].empty_label = None
        self.setup_field(
            'address_adm_level_1',
            country_map.administrative_level_1_endonym,
            country_map.administrative_level_1_mandatory
        )
        self.setup_field(
            'address_adm_level_2',
            country_map.administrative_level_2_endonym,
            country_map.administrative_level_2_mandatory
        )
        self.setup_field(
            'address_adm_level_3',
            country_map.administrative_level_3_endonym,
            country_map.administrative_level_3_mandatory
        )
        self.setup_field(
            'address_adm_level_4',
            country_map.administrative_level_4_endonym,
            country_map.administrative_level_4_mandatory
        )
        self.setup_field(
            'address_adm_level_5',
            country_map.administrative_level_5_endonym,
            country_map.administrative_level_5_mandatory
        )

    def setup_field(self, field_name, value, required):
        if value:
            self.fields[field_name].label = value
            self.fields[field_name].required = required
        else:
            self.fields.pop(field_name)
