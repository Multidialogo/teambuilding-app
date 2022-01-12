from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AccountsTestCase(TestCase):
    def setUp(self):
        # noinspection PyPep8Naming
        User = get_user_model()
        User.objects.create_user('test@example.com', 'test!pwd01', is_active=True)

    def test_password_reset(self):
        response = self.client.get(reverse('password-reset'))
        self.assertEqual(response.status_code, 200)

        post_args = {'email': 'test@example.com'}
        response = self.client.post(reverse('password-reset'), post_args)
        self.assertRedirects(response, reverse('password-reset-done'))
