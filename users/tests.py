from django.conf import settings
from django.test import TestCase
from django.test.client import Client

# Create your tests here.
from products.models import ProductCategory, Product

from users.models import User


def try_to_validate(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            print(f'{func.__name__} is OK')
        except Exception as e:
            print(f'{func.__name__} is NG')
            print(e)

    return wrapper


class TestMainSmokeTest(TestCase):
    status_code_success = 200
    status_code_redirect = 302
    username = 'Alex'
    email = 'Alex@alex.ru'
    password = '1'

    new_user_data = {
        'username': 'Alex',
        'first_name': 'Alex',
        'last_name': 'Alex',
        'password1': '1',
        'password2': '1',
        'email': 'Alex@alex.ru'}

    def setUp(self) -> None:
        self.user = User.objects.create_superuser(self.username, email=self.email, password=self.password)
        self.client = Client()

    @try_to_validate
    def test_main_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)

    @try_to_validate
    def test_is_anonymous(self):
        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_anonymous)

    @try_to_validate
    def test_is_login(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, self.status_code_success)

    @try_to_validate
    def test_register(self):
        response = self.client.post('/users/register/', data=self.new_user_data)
        self.assertEqual(response.status_code, self.status_code_redirect)

        new_user = User.objects.get(username=self.new_user_data['username'])
        activation_url = f"{settings.DOMAIN_NAME}/users/verify/{self.new_user_data['email']}/{new_user.activation_key}/"
        print(activation_url)

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, self.status_code_success)

        new_user.refresh_from_db()
        self.assertTrue(new_user.is_active)

def tearDown(self) -> None:
    pass
