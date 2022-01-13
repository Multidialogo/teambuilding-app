from django.test import TestCase
from django.urls import reverse

from teambuilding.accounts.models import UserAccount
from teambuilding.products.forms import ProductForm
from teambuilding.products.models import Product, Producer
from tests.utils.products import make_producer_post_data, make_producer_request_kwargs
from tests.utils.testutils import model_to_post_data


class FixtureTestCase(TestCase):
    fixtures = ['./tests/fixtures/fixture.yaml', ]

    def login_admin(self):
        admin_user = UserAccount.objects.get(email__exact='admin@example.com')
        admin_login = self.client.login(email='admin@example.com', password='pass1test')
        self.assertTrue(admin_login)
        return admin_user


class AccountsTestCase(FixtureTestCase):
    def test_password_reset(self):
        response = self.client.get(reverse('password-reset'))
        self.assertEqual(response.status_code, 200)

        post_data = {'email': 'test@example.com'}
        request_url = reverse('password-reset')
        response = self.client.post(request_url, post_data)
        self.assertRedirects(response, reverse('password-reset-done'))


class ProductsTestCase(FixtureTestCase):
    def test_admin_can_edit_any_product(self):
        admin_user = self.login_admin()

        product = Product.objects.exclude(added_by_user__account_id=admin_user.id).first()
        product_title_edit = product.title + '(edit)'

        post_data = model_to_post_data(product, ProductForm)
        post_data.update({'title': product_title_edit})
        request_kwargs = {'pk': product.pk}
        request_url = reverse('product-update', kwargs=request_kwargs)

        response = self.client.post(request_url, post_data)
        self.assertRedirects(response, reverse('product-list'))

        product.refresh_from_db()
        self.assertEqual(product.title, product_title_edit)


class ProducersTestCase(FixtureTestCase):
    def test_admin_can_edit_any_producer(self):
        admin_user = self.login_admin()

        producer = Producer.objects.exclude(added_by_user__account_id=admin_user.id).first()
        producer_name_edit = producer.name + '(edit)'

        post_data = make_producer_post_data(producer)
        post_data.update({'name': producer_name_edit})
        request_kwargs = make_producer_request_kwargs(producer)
        request_url = reverse('product-producer-update', kwargs=request_kwargs)

        response = self.client.post(request_url, post_data)
        self.assertRedirects(response, reverse('product-producer-list'))

        producer.refresh_from_db()
        self.assertEqual(producer.name, producer_name_edit)
