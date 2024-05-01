from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from manageuser_app.forms import CustomUserCreationForm, CustomAuthenticationForm

User = get_user_model()


class TestManageUserViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_register_view_post_success(self):
        data = {
            'username': 'test@manageuser.com',
            'email': 'test@manageuser.com',
            'password1': 'testpasswordZ!1',
            'password2': 'testpasswordZ!1',
            'salutation': 'Mr',
            'first_name': 'John',
            'last_name': 'Doe',
            'jobtitle': 'Developer',
            'organisation': 'Tech Co',
            'admin_priv': 0
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='test@manageuser.com').exists())

    def test_register_view_post_failure(self):
        # Invalid data
        data = {
            'username': 'testuser2',
            'email': 'test@mgus.com',
            'password1': 'testpassword',
            'password2': 'invalidpassword',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('password2', response.context['form'].errors)
        self.assertEqual(response.context['form'].errors['password2'][0], 'The two password fields didn’t match.')

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertIsInstance(response.context['form'], CustomAuthenticationForm)

    def test_login_view_post_success(self):
        User.objects.create_user(username='test@manageuser.com', email='test@manageuser.com', password='testpassword')
        data = {
            'email': 'test@manageuser.com',
            'password': 'testpassword',
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 302)  # Redirects to dashboard

    def test_login_view_post_failure(self):
        # Invalid login credentials
        data = {
            'email': 'test@manageuser.com',
            'password': 'invalidpassword',
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid email or password.')

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirects to login page
