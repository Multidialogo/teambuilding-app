import datetime

from teambuilding.products.models import Product


def make_new_event_post_data():
    start_date = datetime.datetime(day=11, month=11, year=2022, hour=18, minute=0)
    end_date = datetime.datetime(day=11, month=11, year=2022, hour=18, minute=30)
    product = Product.objects.first()

    post_data = {
        'title': 'Evento test',
        'description': 'Evento test descritto',
        'start_date': start_date,
        'end_date': end_date,
        'products': (product.pk,),
    }

    return post_data
