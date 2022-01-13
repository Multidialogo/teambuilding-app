from teambuilding.products.forms import ProducerForm, ProducerPostalAddressForm
from tests.utils.testutils import model_to_post_data


def make_new_product_post_data(producer_pk, include_purchase_option=True):
    post_data = {
        'title': 'Prodotto test',
        'description': 'Prodotto test descritto',
        'producer': producer_pk,
    }

    if include_purchase_option:
        option_data = {
            'amount': 'not much',
            'price_cents': 99
        }
        post_data.update(option_data)

    return post_data


def make_new_producer_post_data():
    post_data = {
        'name': 'Produttore test',
        'email': 'produttore@example.com',
        'country': 'IT',
        'zip_code': '63100',
        'street': 'Via dei test 404',
        'adm_level_2': 'TE',
        'adm_level_3': 'Comune test'
    }
    return post_data


def make_producer_post_data(producer):
    producer_data = model_to_post_data(producer, ProducerForm)
    address_data = model_to_post_data(producer.postal_address, ProducerPostalAddressForm)

    post_data = producer_data
    post_data.update(address_data)
    return post_data


def make_producer_request_kwargs(producer):
    request_kwargs = {
        'pk': producer.pk,
        'country': producer.postal_address.country.country_code
    }
    return request_kwargs
