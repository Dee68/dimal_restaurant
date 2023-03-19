from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from account.models import CustomUser, Profile


class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse('account:register')
        self.login_url = reverse('account:signin')
        self.logout_url = reverse('account:logout')
        self.confirm_url = reverse('account:confirmation')
        self.profile_url = reverse('account:profile')
        self.update_profile_url = reverse('account:update-profile')
        self.user = {
            'username':'username',
            'email':'noreply@gmail.com',
            'password1':'password',
            'password2':'password'
        }
        self.user_bad_name = {
            'username': '1abc',
            'email': 'noreply@gmail.com',
            'password1':'password',
            'password2': 'password'
        }
        self.user_with_empty_name = {
            'username':'',
            'email':'noreply@gmail.com',
            'password1':'',
            'password2':'password'
        }
        self.user_with_long_short_name = {
           'username':'username12',
            'email':'noreply@gmail.com',
            'password1':'password',
            'password2':'password' 
        }
        self.user_with_non_alphanumeric = {
            'username':'user@12',
            'email':'noreply@gmail.com',
            'password1':'password',
            'password2':'password'
        }
        self.user_with_no_match_password = {
            'username':'user',
            'email':'noreply@gmail.com',
            'password1':'password1',
            'password2':'password2'
        }
        self.user_with_invalid_email = {
            'username':'user',
            'email':'noreply@com',
            'password1':'password',
            'password2':'password'
        }
        self.user_with_taken_email = {
             'username':'test',
            'email':'noreply@gmail.com',
            'password1':'password',
            'password2':'password'
        }
        self.user_with_taken_name = {
            'username':'username',
            'email':'noreply1@gmail.com',
            'password1':'password',
            'password2':'password'
        }
        self.user_empty_login = {
            'username': '',
            'password': ''
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

    def test_can_not_register_user_with_empty_username(self):
        response = self.client.post(self.register_url, self.user_with_empty_name, format='text/html')
        self.assertEqual(response.status_code, 400)

    def test_can_not_register_user_with_long_short_username(self):
        response = self.client.post(self.register_url, self.user_with_long_short_name, format='text/html')
        self.assertEqual(response.status_code, 406)

    def test_can_not_register_user_with_non_alphanumeric_username(self):
        response = self.client.post(self.register_url, self.user_with_non_alphanumeric, format='text/html')
        self.assertEqual(response.status_code, 400)

    def test_can_not_register_user_with_no_match_password(self):
        response = self.client.post(self.register_url, self.user_with_no_match_password, format='text/html')
        self.assertEqual(response.status_code, 404)

    def test_can_not_register_user_with_invalid_email(self):
        response = self.client.post(self.register_url, self.user_with_invalid_email, format='text/html')
        self.assertEqual(response.status_code, 400)

    def test_can_not_register_user_with_taken_email(self):
        self.client.post(self.register_url, self.user, format='text/html')
        response = self.client.post(self.register_url, self.user_with_taken_email, format='text/html')
        self.assertEqual(response.status_code, 409)

    def test_can_not_register_user_with_taken_name(self):
        self.client.post(self.register_url, self.user, format='text/html')
        response = self.client.post(self.register_url, self.user_with_taken_name, format='text/html')
        self.assertEqual(response.status_code, 409)

    def test_can_not_allow_user_with_number_starts_name(self):
        response = self.client.post(self.register_url, self.user_bad_name, format='text/html')
        self.assertEqual(response.status_code, 400)

class LoginTest(BaseTest):
    def test_show_login_page(self):
        response = self.client.get(self.login_url)
        self.assertTemplateUsed(response, 'account/login.html')
        self.assertEqual(response.status_code, 200)

    def test_empty_inputs_no_signin(self):
        response = self.client.post(self.login_url, self.user_empty_login, format='text/html')
        self.assertEqual(response.status_code, 400)

    def test_signin_user(self):
        self.client.post(self.register_url, self.user, format='text/html')
        username = self.user['username']
        password = self.user['password1']
        self.user_login = {'username':username, 'password': password}
        response = self.client.post(self.login_url, self.user_login)
        self.assertRedirects(response, reverse('restaurant:home'))

    def test_bad_input_signin(self):
        self.user_bad_inputs = {
            'username': 'user#',
            'password': 'password'
        }
        response = self.client.post(self.login_url, self.user_bad_inputs, format='text/html')
        self.assertEqual(response.status_code, 401)

    def test_log_out_user(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/confirm.html')

    def test_user_confirmation(self):
        response = self.client.get(self.confirm_url)
        self.assertTemplateUsed(response, 'account/confirm.html')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.confirm_url,{'yes':'yes'})
        self.assertRedirects(response, reverse('restaurant:home'))
        response = self.client.post(self.confirm_url,{'no':'no'})
        self.assertRedirects(response, reverse('restaurant:home'))
              

class ProfileTest(BaseTest):
    def test_should_create_user_profile(self):
        user = CustomUser.objects.create_user(username='testme', email='noreply@gmail.com', password='password')
        user.set_password('password')
        user.save()
        self.assertEqual(str(user), 'testme')
        pr = Profile.objects.get(user=user)
        self.assertEqual(str(pr), f"{user.username[0].upper()+ user.username[1:]}'s Profile")

    def test_user_open_profile(self):
        self.client.post(self.register_url, self.user, format='text/html')
        username = self.user['username']
        password = self.user['password1']
        self.user_login = {'username':username, 'password': password}
        self.client.post(self.login_url, self.user_login)
        response = self.client.get(self.profile_url)
        self.assertTemplateUsed(response, 'account/profile_page.html')
        

    def test_update_user_profile(self):
        self.client.post(self.register_url, self.user, format='text/html')
        username = self.user['username']
        password = self.user['password1']
        self.user_login = {'username':username, 'password': password}
        self.client.post(self.login_url, self.user_login)
        response = self.client.get(self.update_profile_url)
        self.assertTemplateUsed(response, 'account/update_profile.html')
