from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm

User = get_user_model()

class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('password'))
        self.assertEqual(user.role, 'staff')  # Default role

    def test_user_roles(self):
        manager = User.objects.create_user(username='manager', email='manager@example.com', password='password', role='manager')
        staff = User.objects.create_user(username='staff', email='staff@example.com', password='password', role='staff')
        self.assertEqual(manager.role, 'manager')
        self.assertEqual(staff.role, 'staff')

class AuthViewTest(TestCase):
    def setUp(self):
        self.manager = User.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='password123',
            role='manager'
        )
        self.staff = User.objects.create_user(
            username='staff',
            email='staff@example.com',
            password='password123',
            role='staff'
        )

    def test_login_view_get(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_view_post_correct_credentials(self):
        data = {'username': 'manager', 'password': 'password123'}
        response = self.client.post(reverse('accounts:login'), data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertRedirects(response, '/')

    def test_login_view_post_wrong_credentials(self):
        data = {'username': 'manager', 'password': 'wrongpassword'}
        response = self.client.post(reverse('accounts:login'), data)
        self.assertEqual(response.status_code, 200)  # Stay on login page
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_view(self):
        self.client.login(username='manager', password='password123')
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:login'))

    def test_register_view_get(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_view_post_valid_data(self):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'staff',
            'password1': 'password123',
            'password2': 'password123',
        }
        response = self.client.post(reverse('accounts:register'), data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue(User.objects.filter(username='newuser').exists())
        user = User.objects.get(username='newuser')
        self.assertEqual(user.role, 'staff')

    def test_register_view_post_duplicate_email(self):
        # Create a user first
        User.objects.create_user(username='existing', email='existing@example.com', password='password123')

        data = {
            'username': 'newuser',
            'email': 'existing@example.com',  # Duplicate email
            'first_name': 'New',
            'last_name': 'User',
            'role': 'staff',
            'password1': 'password123',
            'password2': 'password123',
        }
        response = self.client.post(reverse('accounts:register'), data)
        self.assertEqual(response.status_code, 200)  # Stay on register page
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_profile_view_authenticated(self):
        self.client.login(username='manager', password='password123')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_profile_view_unauthenticated(self):
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('accounts:profile')}")

class UserRegisterFormTest(TestCase):
    def test_form_valid_data(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'manager',
            'password1': 'password123',
            'password2': 'password123',
        }
        form = UserRegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_duplicate_username(self):
        User.objects.create_user(username='existing', email='existing@example.com', password='password123')

        data = {
            'username': 'existing',  # Duplicate username
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'staff',
            'password1': 'password123',
            'password2': 'password123',
        }
        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
