from django.test import TestCase, Client
from django.contrib.auth.models import User
from exams.models import ExamSession, ExamFamily
from questions.models import Question, Subject

class LandingTests(TestCase):
    def test_landing_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Prepare Smarter")
        self.assertContains(response, "Questions")

class SearchTests(TestCase):
    def test_search(self):
        response = self.client.get('/search/?q=BCS')
        self.assertEqual(response.status_code, 200)

class AdminDashboardTests(TestCase):
    def test_admin_dashboard_requires_staff(self):
        response = self.client.get('/admin/dashboard/')
        self.assertIn(response.status_code, [302, 403])
        # create staff
        User.objects.create_user('staff', 's@test.com', 'pass', is_staff=True)
        self.client.login(username='staff', password='pass')
        response = self.client.get('/admin/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Admin Dashboard")
