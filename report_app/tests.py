from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from data_app.models import Reference
from .views import all_reports, reference, download_summaries, report_user, report_authors

User = get_user_model()


class TestReportViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testunittest@user.gmail.com',
            email='testunittest@user.gmail.com',
            password='unittest!X1'
        )
        self.client.force_login(self.user)

    def test_all_reports(self):
        response = self.client.get(reverse('all_reports'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_reports.html')

    def test_download_summaries(self):
        response = self.client.get(reverse('download_summaries'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'download_summaries.html')

    def test_report_user(self):
        # Test without query parameters
        response = self.client.get(reverse('report_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report_user.html')

        # Test with query parameters
        response = self.client.get(reverse('report_user'), {'parameter': 'value', 'approval_show': 'approval'})
        self.assertEqual(response.status_code, 200)
        # Add more assertions as needed

    def test_report_authors(self):
        # Test without query parameters
        response = self.client.get(reverse('report_authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report_authors.html')

        # Test with query parameters
        response = self.client.get(reverse('report_authors'), {'selection_id': 'authors'})
        self.assertEqual(response.status_code, 200)
