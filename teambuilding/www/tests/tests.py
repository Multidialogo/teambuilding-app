import datetime
from io import StringIO

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.management import call_command
from django.forms import model_to_dict
from django.test import TestCase
from django.urls import reverse

from teambuilding.events.forms import TasteEventForm
from teambuilding.events.models import TasteEvent
from teambuilding.products.forms import ProductForm, ProducerForm, ProducerPostalAddressForm
from teambuilding.products.models import Product, Producer
from teambuilding.site.models import Notification
from teambuilding.www.tests.utils import model_to_post_data


def login_user(test_case):
    user_email = 'test@example.com'
    user = get_user_model().objects.get(email__exact=user_email)
    user_login = test_case.client.login(email=user_email, password='pass1test')

    test_case.assertTrue(user_login)
    return user.profile


def login_admin(test_case):
    admin_email = 'admin@example.com'
    admin_user = get_user_model().objects.get(email__exact=admin_email)
    admin_login = test_case.client.login(email='admin@example.com', password='pass1test')

    test_case.assertTrue(admin_login)
    return admin_user.profile


class FixtureTestCase(TestCase):
    fixtures = ['./teambuilding/www/tests/fixtures/fixture.yaml', ]


class AccountsTestCase(FixtureTestCase):
    def test_guest_can_signup(self):
        request_url = reverse('signup')
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 200)

        post_data = {
            'nickname': 'Utente',
            'email': 'user@example.com',
            'birth_date': '1990-01-01',
            'password1': 'pass1test',
            'password2': 'pass1test'
        }

        response = self.client.post(request_url, post_data)
        self.assertTemplateUsed(response, template_name='teambuilding/site/auth/signup_success.html')

    def test_user_can_login(self):
        request_url = reverse('login')
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 200)

        login_user(self)

    def test_admin_can_login(self):
        request_url = reverse('login')
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 200)

        admin = login_admin(self)
        self.assertTrue(admin.account.is_superuser)

    def test_password_reset(self):
        request_url = reverse('password-reset')
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 200)

        post_data = {
            'email': 'test@example.com'
        }

        response = self.client.post(request_url, post_data)
        self.assertRedirects(response, reverse('password-reset-done'))


class ProductsTestCase(FixtureTestCase):
    def test_user_can_add_product(self):
        login_user(self)

        request_url = reverse('product-create')
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 200)

        producer = Producer.objects.first()

        post_data = {
            'title': 'Prodotto test',
            'description': 'Prodotto test descritto',
            'producer': producer.pk,
            'amount': 'not much',
            'price_cents': 99
        }

        response = self.client.post(request_url, post_data)
        self.assertRedirects(response, reverse('product-list'))

        product = Product.objects.get(title__exact='Prodotto test')
        self.assertTrue(product)

    def test_user_cant_edit_other_user_product(self):
        user = login_user(self)

        product = Product.objects.exclude(added_by_user__account_id=user.id).first()
        product_data_before = model_to_dict(product)

        request_kwargs = {'pk': product.pk}
        request_url = reverse('product-update', kwargs=request_kwargs)
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 403)

        post_data = model_to_post_data(product, ProductForm)
        post_data.update({'title': product.title + '(edit)'})

        response = self.client.post(request_url, post_data)
        self.assertEqual(response.status_code, 403)

        product.refresh_from_db()
        product_data = model_to_dict(product)
        self.assertEqual(product_data_before, product_data)

    def test_admin_can_edit_any_product(self):
        admin_user = login_admin(self)

        product = Product.objects.exclude(added_by_user__account_id=admin_user.id).first()
        product_data_before = model_to_dict(product)

        request_kwargs = {'pk': product.pk}
        request_url = reverse('product-update', kwargs=request_kwargs)
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 200)

        post_data = model_to_post_data(product, ProductForm)
        post_data.update({'title': product.title + '(edit)'})

        response = self.client.post(request_url, post_data)
        self.assertRedirects(response, reverse('product-list'))

        product.refresh_from_db()
        product_data = model_to_dict(product)
        self.assertNotEqual(product_data_before, product_data)


class ProducersTestCase(FixtureTestCase):
    def test_user_can_add_producer(self):
        login_user(self)

        request_kwargs = {'country': 'IT'}
        request_url = reverse('product-producer-create', kwargs=request_kwargs)
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 200)

        post_data = {
            'name': 'Produttore test',
            'email': 'produttore@example.com',
            'country': 'IT',
            'zip_code': '63100',
            'street': 'Via dei test 404',
            'adm_level_2': 'TE',
            'adm_level_3': 'Comune test'
        }

        response = self.client.post(request_url, post_data)
        self.assertRedirects(response, reverse('product-producer-list'))

        producer = Producer.objects.get(name__exact='Produttore test')
        self.assertTrue(producer)

    def test_user_cant_edit_other_user_producer(self):
        user = login_user(self)

        producer = Producer.objects.exclude(added_by_user_id=user.id).first()
        producer_data_before = model_to_dict(producer)

        request_kwargs = {
            'pk': producer.pk,
            'country': producer.postal_address.country.country_code
        }

        request_url = reverse('product-producer-update', kwargs=request_kwargs)
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 403)

        producer_data = model_to_post_data(producer, ProducerForm)
        address_data = model_to_post_data(producer.postal_address, ProducerPostalAddressForm)
        post_data = producer_data
        post_data.update(address_data)
        post_data.update({'name': producer.name + '(edit)'})

        response = self.client.post(request_url, post_data)
        self.assertEqual(response.status_code, 403)

        producer.refresh_from_db()
        producer_data = model_to_dict(producer)
        self.assertEqual(producer_data_before, producer_data)

    def test_admin_can_edit_any_producer(self):
        admin = login_admin(self)

        producer = Producer.objects.exclude(added_by_user_id=admin.id).first()
        producer_data_before = model_to_dict(producer)

        request_kwargs = {
            'pk': producer.pk,
            'country': producer.postal_address.country.country_code
        }

        request_url = reverse('product-producer-update', kwargs=request_kwargs)
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 200)

        producer_data = model_to_post_data(producer, ProducerForm)
        address_data = model_to_post_data(producer.postal_address, ProducerPostalAddressForm)
        post_data = producer_data
        post_data.update(address_data)
        post_data.update({'name': producer.name + '(edit)'})

        response = self.client.post(request_url, post_data)
        self.assertRedirects(response, reverse('product-producer-list'))

        producer.refresh_from_db()
        producer_data = model_to_dict(producer)
        self.assertNotEqual(producer_data_before, producer_data)


class EventsTestCase(FixtureTestCase):
    def test_user_can_add_event(self):
        login_user(self)

        request_url = reverse('event-create')
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 200)

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

        response = self.client.post(request_url, post_data)
        self.assertRedirects(response, reverse('event-user-list'))

        event = TasteEvent.objects.get(title__exact='Evento test')
        self.assertTrue(event)

    def test_user_cant_edit_other_user_event(self):
        user = login_user(self)

        event = TasteEvent.objects.exclude(organizer_id=user.id).first()
        event_data_before = model_to_dict(event)

        request_kwargs = {'pk': event.pk}
        request_url = reverse('event-update', kwargs=request_kwargs)
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 403)

        post_data = model_to_post_data(event, TasteEventForm)
        post_data.update({'title': event.title + '(edit)'})

        response = self.client.post(request_url, post_data)
        self.assertEqual(response.status_code, 403)

        event.refresh_from_db()
        event_data = model_to_dict(event)
        self.assertEqual(event_data_before, event_data)

    def test_admin_can_edit_any_event(self):
        admin = login_admin(self)

        event = TasteEvent.objects.exclude(organizer_id=admin.id).first()
        event_data_before = model_to_dict(event)

        request_kwargs = {'pk': event.pk}
        request_url = reverse('event-update', kwargs=request_kwargs)
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 200)

        event_data = model_to_post_data(event, TasteEventForm)
        event_data['products'] = [product.pk for product in event_data['products']]
        post_data = event_data
        post_data.update({'title': event.title + '(edit)', 'products': [1]})

        response = self.client.post(request_url, post_data)
        self.assertRedirects(response, reverse('event-user-list'))

        event.refresh_from_db()
        event_data = model_to_dict(event)
        self.assertNotEqual(event_data_before, event_data)


class SiteTestCase(FixtureTestCase):
    def test_users_birthday_check_command(self):
        today_date = datetime.date.today()
        yesterday_date = today_date - datetime.timedelta(days=1)
        tomorrow_date = today_date + datetime.timedelta(days=1)
        four_days_date = today_date + datetime.timedelta(days=4)
        seven_days_date = today_date + datetime.timedelta(days=7)

        fixture_users = get_user_model().objects.all()

        for fixture_user in fixture_users:
            fixture_user.birth_date = yesterday_date
            fixture_user.save()

        get_user_model().objects.create_user(
            'celebrated@example.com',
            'pass1test',
            birth_date=today_date
        )
        get_user_model().objects.create_user(
            'almostcelebrated@example.com',
            'pass1test',
            birth_date=tomorrow_date
        )
        get_user_model().objects.create_user(
            'unluckycelebrated@example.com',
            'pass1test',
            birth_date=four_days_date
        )
        get_user_model().objects.create_user(
            'oneweekcelebrated@example.com',
            'pass1test',
            birth_date=seven_days_date
        )

        notification_count_before = Notification.objects.count()
        email_sent_count_before = len(mail.outbox)

        out = StringIO()

        with self.captureOnCommitCallbacks(execute=True):
            call_command('users_birthday_check', stdout=out)

        notification_count_after = Notification.objects.count()
        notifications_sent_count = notification_count_after - notification_count_before

        email_sent_count_after = len(mail.outbox)
        email_sent_count = email_sent_count_after - email_sent_count_before

        self.assertIn("Birthday check done.", out.getvalue())
        # total 7 users, 1 birthday today, 1 birthday tomorrow, 1 birthday in 7 days
        # 1 happy bday + 6 happy bday reminders + 6 one-day reminders + 6 seven-days reminders
        self.assertEqual(notifications_sent_count, 19)
        # 1 happy bday + 6 reminders
        self.assertEqual(email_sent_count, 7)

    def test_wish_happy_birthday(self):
        login_user(self)

        today_date = datetime.date.today()
        birthday_user = get_user_model().objects.create_user(
            'celebrated@example.com',
            'pass1test',
            birth_date=today_date
        )

        request_kwargs = {'bday_user_pk': birthday_user.pk}
        request_url = reverse('user-profile-happy-bday', kwargs=request_kwargs)
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 200)

        yesterday_date = today_date - datetime.timedelta(days=1)
        not_birthday_user = get_user_model().objects.create_user(
            'notcelebrated@example.com',
            'pass1test',
            birth_date=yesterday_date
        )

        request_kwargs = {'bday_user_pk': not_birthday_user.pk}
        request_url = reverse('user-profile-happy-bday', kwargs=request_kwargs)
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, 403)
