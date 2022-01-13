from django.forms import model_to_dict
from django.test import TestCase
from django.urls import reverse

from teambuilding.accounts.models import UserAccount
from teambuilding.products.models import Product


class FixtureTestCase(TestCase):
    fixtures = ['./tests/teambuilding/fixtures/fixture.yaml', ]


class AccountsTestCase(FixtureTestCase):
    def test_password_reset(self):
        response = self.client.get(reverse('password-reset'))
        self.assertEqual(response.status_code, 200)

        post_args = {'email': 'test@example.com'}
        response = self.client.post(reverse('password-reset'), post_args)
        self.assertRedirects(response, reverse('password-reset-done'))


class ProductsTestCase(FixtureTestCase):
    def test_admin_can_edit_any_product(self):
        admin_user = UserAccount.objects.get(email__exact='admin@example.com')
        admin_login = self.client.login(email='admin@example.com', password='pass1test')
        self.assertTrue(admin_login)

        product = Product.objects.exclude(added_by_user__account_id=admin_user.id).first()
        product_title_edit = product.title + '(edit)'
        post_args = model_to_dict(product)
        post_args.update({'title': product_title_edit})
        post_url = reverse('product-update', kwargs={'pk': product.pk})

        response = self.client.post(post_url, post_args)
        self.assertEqual(response.request.user.id, admin_user.id)
        self.assertRedirects(response, reverse('product-list'))

        product.refresh_from_db()
        self.assertEqual(product.title, product_title_edit)
