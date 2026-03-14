from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from core.models import Product, Supplier, StockMovement

User = get_user_model()


class ProductModelTest(TestCase):
    def setUp(self):
        self.manager = User.objects.create_user(
            username='manager', password='password', role='manager'
        )
        self.supplier = Supplier.objects.create(
            name='Test Supplier',
            contact_person='John Doe',
            email='john@test.com',
            phone='123-456-7890',
            address='123 Test St',
            created_by=self.manager
        )

    def test_product_creation(self):
        product = Product.objects.create(
            name='Test Product',
            description='A test product',
            unit_price=15.00,
            stock_quantity=100,
            supplier=self.supplier,
            created_by=self.manager
        )
        self.assertEqual(product.name, 'Test Product')
        self.assertTrue(product.is_active)


class SupplierViewTest(TestCase):
    def setUp(self):
        self.manager = User.objects.create_user(
            username='manager', password='password', role='manager'
        )
        self.staff = User.objects.create_user(
            username='staff', password='password', role='staff'
        )
        self.supplier = Supplier.objects.create(
            name='Test Supplier',
            contact_person='John Doe',
            email='john@test.com',
            phone='123-456-7890',
            address='123 Test St',
            created_by=self.manager
        )

    def test_supplier_list_view(self):
        self.client.login(username='staff', password='password')
        response = self.client.get(reverse('core:supplier_list'))
        self.assertEqual(response.status_code, 200)

    def test_supplier_detail_view(self):
        self.client.login(username='staff', password='password')
        response = self.client.get(reverse('core:supplier_detail', args=[self.supplier.pk]))
        self.assertEqual(response.status_code, 200)

    def test_supplier_create_view_manager(self):
        self.client.login(username='manager', password='password')
        data = {
            'name': 'New Supplier',
            'contact_person': 'Jane Smith',
            'email': 'jane@newsupplier.com',
            'phone': '987-654-3210',
            'address': '456 New St',
            'is_active': True,
            'notes': 'Test supplier',
        }
        response = self.client.post(reverse('core:supplier_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Supplier.objects.filter(name='New Supplier').exists())

    def test_supplier_create_view_staff_denied(self):
        self.client.login(username='staff', password='password')
        response = self.client.get(reverse('core:supplier_create'))
        self.assertEqual(response.status_code, 302)

    def test_supplier_update_view_manager(self):
        self.client.login(username='manager', password='password')
        data = {
            'name': 'Updated Supplier',
            'contact_person': 'John Doe',
            'email': 'john@test.com',
            'phone': '123-456-7890',
            'address': '123 Test St',
            'is_active': True,
            'notes': 'Updated notes',
        }
        response = self.client.post(
            reverse('core:supplier_update', args=[self.supplier.pk]), data
        )
        self.assertEqual(response.status_code, 302)
        self.supplier.refresh_from_db()
        self.assertEqual(self.supplier.name, 'Updated Supplier')


class ProductViewTest(TestCase):
    def setUp(self):
        self.manager = User.objects.create_user(
            username='manager', password='password', role='manager'
        )
        self.staff = User.objects.create_user(
            username='staff', password='password', role='staff'
        )
        self.supplier = Supplier.objects.create(
            name='Test Supplier',
            contact_person='John Doe',
            email='john@test.com',
            phone='123-456-7890',
            address='123 Test St',
            created_by=self.manager
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='A test product',
            unit_price=15.00,
            stock_quantity=100,
            supplier=self.supplier,
            created_by=self.manager
        )

    def test_product_list_view(self):
        self.client.login(username='staff', password='password')
        response = self.client.get(reverse('core:product_list'))
        self.assertEqual(response.status_code, 200)

    def test_product_list_view_with_search(self):
        self.client.login(username='staff', password='password')
        response = self.client.get(reverse('core:product_list') + '?search=Test')
        self.assertEqual(response.status_code, 200)

    def test_product_list_view_with_supplier_filter(self):
        self.client.login(username='staff', password='password')
        response = self.client.get(
            reverse('core:product_list') + f'?supplier_id={self.supplier.pk}'
        )
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view(self):
        self.client.login(username='staff', password='password')
        response = self.client.get(reverse('core:product_detail', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)

    def test_product_create_view_manager(self):
        self.client.login(username='manager', password='password')
        data = {
            'name': 'New Product',
            'description': 'A new product',
            'unit_price': '20.00',
            'stock_quantity': 50,
            'supplier': self.supplier.pk,
            'is_active': True,
        }
        response = self.client.post(reverse('core:product_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(name='New Product').exists())

    def test_product_create_view_invalid_data(self):
        self.client.login(username='manager', password='password')
        data = {
            'name': '',
            'unit_price': '20.00',
            'stock_quantity': 50,
            'supplier': self.supplier.pk,
        }
        response = self.client.post(reverse('core:product_create'), data)
        self.assertEqual(response.status_code, 200)

    def test_product_create_view_staff_denied(self):
        self.client.login(username='staff', password='password')
        response = self.client.get(reverse('core:product_create'))
        self.assertEqual(response.status_code, 302)

    def test_product_update_view_manager(self):
        self.client.login(username='manager', password='password')
        data = {
            'name': 'Updated Product',
            'description': 'An updated product',
            'unit_price': '18.00',
            'stock_quantity': 100,
            'supplier': self.supplier.pk,
            'is_active': True,
        }
        response = self.client.post(
            reverse('core:product_update', args=[self.product.pk]), data
        )
        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')