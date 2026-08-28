from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class AuthTests(TestCase):
    def test_register(self):
        resp = self.client.post('/accounts/register/', {'username': 'newuser', 'email': 'new@test.com', 'password1': 'ComplexPass123!', 'password2': 'ComplexPass123!'})
        self.assertIn(resp.status_code, [302, 200])
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login(self):
        User.objects.create_user('loginuser', 'l@test.com', 'pass123')
        resp = self.client.post('/accounts/login/', {'username': 'loginuser', 'password': 'pass123'})
        self.assertIn(resp.status_code, [302, 200])

    def test_profile_requires_login(self):
        resp = self.client.get('/accounts/profile/')
        self.assertEqual(resp.status_code, 302)
        User.objects.create_user('u2', 'u2@test.com', 'pass')
        self.client.login(username='u2', password='pass')
        resp = self.client.get('/accounts/profile/')
        self.assertEqual(resp.status_code, 200)

    def test_permissions(self):
        # non-staff cannot access import upload
        User.objects.create_user('normal', 'n@test.com', 'pass')
        self.client.login(username='normal', password='pass')
        resp = self.client.get('/imports/upload/')
        self.assertIn(resp.status_code, [302, 403])
