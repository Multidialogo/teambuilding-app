from django.forms import model_to_dict
from django.test import TestCase
from django.urls import reverse

from teambuilding.accounts.models import UserAccount
from teambuilding.events.forms import TasteEventForm
from teambuilding.events.models import TasteEvent
from teambuilding.products.forms import ProductForm
from teambuilding.products.models import Product, Producer
from tests.utils.products import make_producer_post_data, make_producer_request_kwargs
from tests.utils.testutils import model_to_post_data


class FixtureTestCase(TestCase):
    fixtures = ['./tests/fixtures/fixture.yaml', ]

    def login_user(self):
        user_email = 'test@example.com'
        user = UserAccount.objects.get(email__exact=user_email)
        user_login = self.client.login(email=user_email, password='pass1test')

        self.assertTrue(user_login)
        return user.profile

    def login_admin(self):
        admin_email = 'admin@example.com'
        admin_user = UserAccount.objects.get(email__exact=admin_email)
        admin_login = self.client.login(email='admin@example.com', password='pass1test')

        self.assertTrue(admin_login)
        return admin_user.profile


class AccountsTestCase(FixtureTestCase):
    def test_password_reset(self):
        response = self.client.get(reverse('password-reset'))
        self.assertEqual(response.status_code, 200)

        post_data = {'email': 'test@example.com'}
        request_url = reverse('password-reset')
        response = self.client.post(request_url, post_data)
        self.assertRedirects(response, reverse('password-reset-done'))


class ProductsTestCase(FixtureTestCase):
    def test_user_cant_edit_other_user_product(self):
        user = self.login_user()

        product = Product.objects.exclude(added_by_user__account_id=user.id).first()
        model_data_before = model_to_dict(product)

        post_data = model_to_post_data(product, ProductForm)
        post_data.update({'title': product.title + '(edit)'})
        request_kwargs = {'pk': product.pk}
        request_url = reverse('product-update', kwargs=request_kwargs)

        response = self.client.post(request_url, post_data)
        self.assertEqual(response.status_code, 403)

        product.refresh_from_db()
        model_data = model_to_dict(product)
        self.assertEqual(model_data_before, model_data)

    def test_admin_can_edit_any_product(self):
        admin_user = self.login_admin()

        product = Product.objects.exclude(added_by_user__account_id=admin_user.id).first()
        model_data_before = model_to_dict(product)

        post_data = model_to_post_data(product, ProductForm)
        post_data.update({'title': product.title + '(edit)'})
        request_kwargs = {'pk': product.pk}
        request_url = reverse('product-update', kwargs=request_kwargs)

        response = self.client.post(request_url, post_data)
        self.assertRedirects(response, reverse('product-list'))

        product.refresh_from_db()
        model_data = model_to_dict(product)
        self.assertNotEqual(model_data_before, model_data)


class ProducersTestCase(FixtureTestCase):
    def test_admin_can_edit_any_producer(self):
        admin = self.login_admin()

        producer = Producer.objects.exclude(added_by_user_id=admin.id).first()
        model_data_before = model_to_dict(producer)

        post_data = make_producer_post_data(producer)
        post_data.update({'name': producer.name + '(edit)'})
        request_kwargs = make_producer_request_kwargs(producer)
        request_url = reverse('product-producer-update', kwargs=request_kwargs)

        response = self.client.post(request_url, post_data)
        self.assertRedirects(response, reverse('product-producer-list'))

        producer.refresh_from_db()
        model_data = model_to_dict(producer)
        self.assertNotEqual(model_data_before, model_data)


class EventsTestCase(FixtureTestCase):
    def test_user_cant_edit_other_user_event(self):
        user = self.login_user()

        event = TasteEvent.objects.exclude(organizer_id=user.id).first()
        model_data_before = model_to_dict(event)

        post_data = model_to_post_data(event, TasteEventForm)
        post_data.update({'title': event.title + '(edit)'})
        request_kwargs = {'pk': event.pk}
        request_url = reverse('event-update', kwargs=request_kwargs)

        response = self.client.post(request_url, request_kwargs)
        self.assertEqual(response.status_code, 403)

        event.refresh_from_db()
        model_data = model_to_dict(event)
        self.assertEqual(model_data_before, model_data)
