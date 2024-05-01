from django.urls import reverse
from django.test import TestCase
from .models import Element

from django.contrib.auth import get_user_model

User = get_user_model()


class TestViews(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testunittest@user.gmail.com',
            email='testunittest@user.gmail.com',
            password='unittest!X1'
        )
        login_success = self.client.login(username='testunittest@user.gmail.com', password='unittest!X1')
        assert login_success, "User failed to log in"

    def test_register_success(self):
        response = self.client.post(reverse('register'), {
            'email': 'newuser@test.com',
            'password1': 'complexpasswordY/1',
            'password2': 'complexpasswordY/1',
            'first_name': 'Test',
            'last_name': 'Doe',
            'salutation': 'Mr',
            'job_title': 'Developer',
            'organisation': 'Tech Co',
            'admin_priv': 0
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='newuser@test.com').exists())

    def test_register_failure(self):
        response = self.client.post(reverse('register'), {
            'email': 'newuser@test.com',
            'password1': 'password',
            'password2': 'password',
            'first_name': 'Test',
            'last_name': 'Doe',
            'salutation': 'Mr',
            'job_title': 'Developer',
            'organisation': 'Tech Co',
            'admin_priv': 0
        })
        self.assertEqual(response.status_code, 200)  # Expecting failure, should render the form again, not redirect
        self.assertIn('password2', response.context['form'].errors)

    def test_tables_panel_get(self):
        response = self.client.get(reverse('tables_panel'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tables_panel.html')

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser@example.com',
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Invalid email or password' in response.content.decode())

    def test_logout(self):
        self.client.login(username='testuser@example.com', email='testuser@example.com', password='password123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))


class TestModels(TestCase):
    def test_element_creation(self):
        element = Element.objects.create(element_symbol="Hydrogen")
        self.assertEqual(element.element_symbol, "Hydrogen")
