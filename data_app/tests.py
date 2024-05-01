from django.test import TestCase, Client
from django.urls import reverse
# from .models import User

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

    def test_tables_panel_get(self):
        response = self.client.get(reverse('tables_panel'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tables_panel.html')


class TestModels(TestCase):
    def test_element_creation(self):
        element = Element.objects.create(element_symbol="Hydrogen")
        self.assertEqual(element.element_symbol, "Hydrogen")
