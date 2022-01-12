from django.test import TestCase
from django.urls import reverse


class FixtureTestCase(TestCase):
    fixtures = ['./tests/teambuilding/fixtures/fixture.yaml', ]


class AccountsTestCase(FixtureTestCase):
    def test_password_reset(self):
        response = self.client.get(reverse('password-reset'))
        self.assertEqual(response.status_code, 200)

        post_args = {'email': 'test@example.com'}
        response = self.client.post(reverse('password-reset'), post_args)
        self.assertRedirects(response, reverse('password-reset-done'))
