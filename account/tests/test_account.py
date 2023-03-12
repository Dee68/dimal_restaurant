from django.test import TestCase
from django.urls import reverse
from account.models import CustomUser, Profile


class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse('account:register')
        self.login_url = reverse('account:signin')
        self.user = {
            'username':'username',
            'email':'noreply@gmail.com',
            'password1':'password',
            'password2':'password'
        }
        return super().setUp()


class RegisterTest(BaseTest):
    def test_show_register_page(self):
        response = self.client.get(self.register_url)
        self.assertTemplateUsed(response, 'account/register.html')
        self.assertEqual(response.status_code, 200)

    def test_can_create_user(self):
        response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertRedirects(response, self.login_url)


class LoginTest(BaseTest):
    def test_show_login_page(self):
        response = self.client.get(self.login_url)
        self.assertTemplateUsed(response, 'account/login.html')
        self.assertEqual(response.status_code, 200)