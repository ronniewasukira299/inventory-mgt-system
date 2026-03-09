from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Category, Device, Tag

User = get_user_model()

class DeviceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.tag = Tag.objects.create(name='Test Tag', slug='test-tag')

    def test_device_creation(self):
        device = Device.objects.create(
            name='Test Device',
            type='serial',
            description='A test device',
            specs={'key': 'value'},
            category=self.category,
            created_by=self.user
        )
        device.tags.add(self.tag)
        self.assertEqual(device.name, 'Test Device')
        self.assertEqual(device.type, 'serial')

class DeviceViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.device = Device.objects.create(
            name='Test Device',
            type='serial',
            description='A test device',
            specs={'key': 'value'},
            category=self.category,
            created_by=self.user
        )

    def test_device_list_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('core:device_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Device')

    def test_device_detail_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('core:device_detail', args=[self.device.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Device')
