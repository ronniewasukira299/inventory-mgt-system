from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('password'))

class AuthViewTest(TestCase):
    def test_login_view(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_post(self):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'password123',
            'password2': 'password123',
            'role': 'viewer'
        }
        response = self.client.post(reverse('accounts:register'), data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(User.objects.filter(username='newuser').exists())
