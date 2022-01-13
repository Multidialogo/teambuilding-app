from teambuilding.products.forms import ProducerForm, ProducerPostalAddressForm
from tests.utils.testutils import model_to_post_data


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
