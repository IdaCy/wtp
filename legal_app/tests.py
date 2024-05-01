from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class TestLegalViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='unittest!X1'
        )
        self.client.login(username='testuser', password='unittest!X1')

    def test_privacy_policy(self):
        response = self.client.get(reverse('privacy_policy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'privacy_policy.html')

    def test_legal_disclaimer(self):
        response = self.client.get(reverse('legal_disclaimer'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'legal_disclaimer.html')
