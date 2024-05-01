from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class TestDashboardViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testunittestd@user.gmail.com',
            email='testunittestd@user.gmail.com',
            password='unittest!X1'
        )
        self.client.force_login(self.user)

    def test_board_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
