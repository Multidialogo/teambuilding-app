from django import forms
from django.forms.models import inlineformset_factory

from services.postal_address.localization import localize_formset
from services.postal_address.services import safe_country_code
from .models import Producer, Product, ProductPurchaseOption, ProducerPostalAddress


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()


class PurchaseOptionForm(forms.ModelForm):
    class Meta:
        model = ProductPurchaseOption
        exclude = ('product',)

    def __init__(self, *arg, **kwarg):
        super(PurchaseOptionForm, self).__init__(*arg, **kwarg)
        self.empty_permitted = False


class ProductPurchaseOptionFormsetFactory:
    def __init__(self, min_num=0, *args, **kwargs):
        self.min_num = min_num

    def make(self, request=None, instance=None, extra=0):
        builder = inlineformset_factory(
            Product, ProductPurchaseOption, form=PurchaseOptionForm, min_num=self.min_num,
            validate_min=True, extra=extra, can_delete=True
        )
        return builder(request or None, instance=instance)


class ProducerForm(forms.ModelForm):
    class Meta:
        model = Producer
        exclude = ()


class ProducerPostalAddressForm(forms.ModelForm):
    class Meta:
        model = ProducerPostalAddress
        exclude = ('producer',)

    def __init__(self, *arg, **kwarg):
        super(ProducerPostalAddressForm, self).__init__(*arg, **kwarg)
        self.empty_permitted = False


class ProducerPostalAddressFormsetFactory:
    def __init__(self, min_num=1, max_num=1):
        self.min_num = min_num
        self.max_num = max_num

    def make(self, country_code=None, request=None, instance=None, extra=0):
        builder = inlineformset_factory(
            Producer, ProducerPostalAddress, form=ProducerPostalAddressForm, min_num=self.min_num,
            validate_min=True, extra=extra, can_delete=False, max_num=self.max_num, validate_max=True
        )
        country_code = safe_country_code(country_code)
        raw = builder(request or None, instance=instance)
        return localize_formset(country_code, raw)
