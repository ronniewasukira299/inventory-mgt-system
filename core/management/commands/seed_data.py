from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from core.models import (
    Supplier, Customer, Category, Tag, Product, Stock, StockMovement,
    Invoice, InvoiceItem, Receipt, ReceiptItem, Debt, DebtPayment,
    AuditLog, ManagerDashboardMetrics
)
from accounts.models import User
import random

class Command(BaseCommand):
    help = 'Seed the database with sample data for all core models'

    def handle(self, *args, **options):
        self.stdout.write('Starting database seeding...')

        # Create users
        self.create_users()

        # Create categories and tags
        categories = self.create_categories_and_tags()

        # Create suppliers
        suppliers = self.create_suppliers()

        # Create customers
        customers = self.create_customers()

        # Create products
        products = self.create_products(categories, suppliers)

        # Create stock records
        self.create_stock(products)

        # Create stock movements
        self.create_stock_movements(products)

        # Create invoices and invoice items
        self.create_invoices_and_items(customers, products)

        # Create receipts and receipt items
        self.create_receipts_and_items(suppliers, products)

        # Create debts and debt payments
        self.create_debts_and_payments()

        # Create audit logs
        self.create_audit_logs()

        # Create dashboard metrics
        self.create_dashboard_metrics()

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded database with sample data')
        )

    def create_users(self):
        """Create sample users"""
        users_data = [
            {'username': 'manager1', 'email': 'manager@example.com', 'role': 'admin', 'first_name': 'John', 'last_name': 'Manager'},
            {'username': 'staff1', 'email': 'staff@example.com', 'role': 'editor', 'first_name': 'Jane', 'last_name': 'Staff'},
            {'username': 'viewer1', 'email': 'viewer@example.com', 'role': 'viewer', 'first_name': 'Bob', 'last_name': 'Viewer'},
        ]

        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'role': user_data['role'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'is_staff': user_data['role'] in ['admin', 'editor'],
                    'is_superuser': user_data['role'] == 'admin',
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)

        self.stdout.write(f'Created {len(users)} users')
        return users

    def create_categories_and_tags(self):
        """Create sample categories and tags"""
        categories_data = [
            {'name': 'Electronics', 'description': 'Electronic components and devices', 'slug': 'electronics'},
            {'name': 'Office Supplies', 'description': 'Office and stationery items', 'slug': 'office-supplies'},
            {'name': 'Furniture', 'description': 'Office and home furniture', 'slug': 'furniture'},
            {'name': 'Tools', 'description': 'Hand tools and equipment', 'slug': 'tools'},
            {'name': 'Books', 'description': 'Books and publications', 'slug': 'books'},
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories.append(category)

        tags_data = [
            {'name': 'New', 'slug': 'new'},
            {'name': 'Bestseller', 'slug': 'bestseller'},
            {'name': 'Discounted', 'slug': 'discounted'},
            {'name': 'Fragile', 'slug': 'fragile'},
            {'name': 'Heavy', 'slug': 'heavy'},
        ]

        tags = []
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(
                name=tag_data['name'],
                defaults={'slug': tag_data['slug']}
            )
            tags.append(tag)

        self.stdout.write(f'Created {len(categories)} categories and {len(tags)} tags')
        return categories

    def create_suppliers(self):
        """Create sample suppliers"""
        suppliers_data = [
            {
                'name': 'TechCorp Supplies',
                'contact_person': 'Alice Johnson',
                'email': 'alice@techcorp.com',
                'phone': '+1-555-0101',
                'address': '123 Tech Street',
                'city': 'San Francisco',
                'country': 'USA',
                'postal_code': '94105',
                'rating': Decimal('4.5'),
                'status': 'active',
                'credit_terms_days': 30,
                'notes': 'Reliable electronics supplier',
            },
            {
                'name': 'OfficeMart',
                'contact_person': 'Bob Smith',
                'email': 'bob@officemart.com',
                'phone': '+1-555-0102',
                'address': '456 Office Ave',
                'city': 'New York',
                'country': 'USA',
                'postal_code': '10001',
                'rating': Decimal('4.2'),
                'status': 'active',
                'credit_terms_days': 45,
                'notes': 'Good for office supplies',
            },
            {
                'name': 'Global Traders',
                'contact_person': 'Carol Davis',
                'email': 'carol@globaltraders.com',
                'phone': '+1-555-0103',
                'address': '789 Trade Blvd',
                'city': 'London',
                'country': 'UK',
                'postal_code': 'SW1A 1AA',
                'rating': Decimal('3.8'),
                'status': 'active',
                'credit_terms_days': 60,
                'notes': 'International supplier',
            },
        ]

        suppliers = []
        manager = User.objects.filter(role='admin').first()
        for supplier_data in suppliers_data:
            supplier, created = Supplier.objects.get_or_create(
                name=supplier_data['name'],
                defaults={
                    **supplier_data,
                    'created_by': manager,
                }
            )
            suppliers.append(supplier)

        self.stdout.write(f'Created {len(suppliers)} suppliers')
        return suppliers

    def create_customers(self):
        """Create sample customers"""
        customers_data = [
            {
                'name': 'ABC Corporation',
                'contact_person': 'David Wilson',
                'email': 'david@abc.com',
                'phone': '+1-555-0201',
                'address': '321 Business St',
                'city': 'Chicago',
                'country': 'USA',
                'postal_code': '60601',
                'credit_limit': Decimal('50000.00'),
                'status': 'active',
                'credit_terms_days': 30,
                'notes': 'Long-term customer',
            },
            {
                'name': 'XYZ Industries',
                'contact_person': 'Emma Brown',
                'email': 'emma@xyz.com',
                'phone': '+1-555-0202',
                'address': '654 Industry Rd',
                'city': 'Houston',
                'country': 'USA',
                'postal_code': '77001',
                'credit_limit': Decimal('75000.00'),
                'status': 'active',
                'credit_terms_days': 45,
                'notes': 'Growing business',
            },
            {
                'name': 'SmallBiz Ltd',
                'contact_person': 'Frank Miller',
                'email': 'frank@smallbiz.com',
                'phone': '+1-555-0203',
                'address': '987 Small St',
                'city': 'Boston',
                'country': 'USA',
                'postal_code': '02101',
                'credit_limit': Decimal('25000.00'),
                'status': 'active',
                'credit_terms_days': 15,
                'notes': 'Small but reliable',
            },
        ]

        customers = []
        manager = User.objects.filter(role='admin').first()
        for customer_data in customers_data:
            customer, created = Customer.objects.get_or_create(
                name=customer_data['name'],
                defaults={
                    **customer_data,
                    'created_by': manager,
                }
            )
            customers.append(customer)

        self.stdout.write(f'Created {len(customers)} customers')
        return customers

    def create_products(self, categories, suppliers):
        """Create sample products"""
        products_data = [
            {
                'code': 'PROD001',
                'name': 'Wireless Mouse',
                'description': 'Ergonomic wireless mouse with USB receiver',
                'category': categories[0],  # Electronics
                'cost_price': Decimal('15.50'),
                'selling_price': Decimal('29.99'),
                'unit': 'piece',
                'quantity_in_stock': 150,
                'reorder_level': 20,
                'reorder_quantity': 100,
                'default_supplier': suppliers[0],
                'specs': {'color': 'black', 'battery_life': '12 months'},
            },
            {
                'code': 'PROD002',
                'name': 'Office Chair',
                'description': 'Comfortable ergonomic office chair',
                'category': categories[2],  # Furniture
                'cost_price': Decimal('120.00'),
                'selling_price': Decimal('249.99'),
                'unit': 'piece',
                'quantity_in_stock': 25,
                'reorder_level': 5,
                'reorder_quantity': 20,
                'default_supplier': suppliers[1],
                'specs': {'material': 'mesh', 'adjustable': True},
            },
            {
                'code': 'PROD003',
                'name': 'Printer Paper A4',
                'description': '500 sheets of 80gsm printer paper',
                'category': categories[1],  # Office Supplies
                'cost_price': Decimal('4.50'),
                'selling_price': Decimal('8.99'),
                'unit': 'box',
                'quantity_in_stock': 200,
                'reorder_level': 50,
                'reorder_quantity': 500,
                'default_supplier': suppliers[1],
                'specs': {'size': 'A4', 'gsm': 80},
            },
            {
                'code': 'PROD004',
                'name': 'Screwdriver Set',
                'description': 'Professional screwdriver set with 12 pieces',
                'category': categories[3],  # Tools
                'cost_price': Decimal('25.00'),
                'selling_price': Decimal('49.99'),
                'unit': 'set',
                'quantity_in_stock': 75,
                'reorder_level': 10,
                'reorder_quantity': 50,
                'default_supplier': suppliers[2],
                'specs': {'pieces': 12, 'material': 'chrome vanadium'},
            },
            {
                'code': 'PROD005',
                'name': 'Python Programming Book',
                'description': 'Comprehensive guide to Python programming',
                'category': categories[4],  # Books
                'cost_price': Decimal('35.00'),
                'selling_price': Decimal('69.99'),
                'unit': 'piece',
                'quantity_in_stock': 45,
                'reorder_level': 8,
                'reorder_quantity': 30,
                'default_supplier': suppliers[2],
                'specs': {'pages': 450, 'edition': '3rd'},
            },
        ]

        products = []
        manager = User.objects.filter(role='admin').first()
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                code=product_data['code'],
                defaults={
                    **product_data,
                    'created_by': manager,
                }
            )
            # Add random tags
            tags = Tag.objects.all()
            if tags:
                product.tags.set(random.sample(list(tags), min(2, len(tags))))
            products.append(product)

        self.stdout.write(f'Created {len(products)} products')
        return products

    def create_stock(self, products):
        """Create stock records for products"""
        for product in products:
            stock, created = Stock.objects.get_or_create(
                product=product,
                defaults={
                    'quantity': product.quantity_in_stock,
                    'location': 'Main Warehouse',
                    'last_counted_at': timezone.now(),
                }
            )

        self.stdout.write(f'Created stock records for {len(products)} products')

    def create_stock_movements(self, products):
        """Create sample stock movements"""
        movements_data = [
            {'product': products[0], 'movement_type': 'in', 'quantity': 100, 'reference_type': 'receipt', 'reference_id': 1, 'notes': 'Initial stock'},
            {'product': products[1], 'movement_type': 'in', 'quantity': 20, 'reference_type': 'receipt', 'reference_id': 2, 'notes': 'Restock'},
            {'product': products[2], 'movement_type': 'out', 'quantity': 50, 'reference_type': 'invoice', 'reference_id': 1, 'notes': 'Sale'},
            {'product': products[3], 'movement_type': 'adjustment', 'quantity': 5, 'reference_type': 'adjustment', 'reference_id': 1, 'notes': 'Inventory correction'},
            {'product': products[4], 'movement_type': 'in', 'quantity': 25, 'reference_type': 'receipt', 'reference_id': 3, 'notes': 'New shipment'},
        ]

        movements = []
        manager = User.objects.filter(role='admin').first()
        for movement_data in movements_data:
            movement = StockMovement.objects.create(
                **movement_data,
                created_by=manager
            )
            movements.append(movement)

        self.stdout.write(f'Created {len(movements)} stock movements')

    def create_invoices_and_items(self, customers, products):
        """Create sample invoices and invoice items"""
        invoices_data = [
            {
                'invoice_number': 'INV001',
                'customer': customers[0],
                'issue_date': timezone.now().date(),
                'due_date': timezone.now().date() + timezone.timedelta(days=30),
                'subtotal': Decimal('89.97'),
                'tax_amount': Decimal('8.99'),
                'total_amount': Decimal('98.96'),
                'paid_amount': Decimal('98.96'),
                'status': 'paid',
                'is_approved': True,
                'approved_by': User.objects.filter(role='admin').first(),
                'approved_at': timezone.now(),
                'notes': 'Paid in full',
            },
            {
                'invoice_number': 'INV002',
                'customer': customers[1],
                'issue_date': timezone.now().date(),
                'due_date': timezone.now().date() + timezone.timedelta(days=45),
                'subtotal': Decimal('249.99'),
                'tax_amount': Decimal('25.00'),
                'total_amount': Decimal('274.99'),
                'paid_amount': Decimal('0.00'),
                'status': 'issued',
                'is_approved': True,
                'approved_by': User.objects.filter(role='admin').first(),
                'approved_at': timezone.now(),
                'notes': 'Awaiting payment',
            },
        ]

        manager = User.objects.filter(role='admin').first()
        for invoice_data in invoices_data:
            invoice, created = Invoice.objects.get_or_create(
                invoice_number=invoice_data['invoice_number'],
                defaults={
                    **invoice_data,
                    'created_by': manager,
                }
            )

            # Create invoice items
            if invoice.invoice_number == 'INV001':
                InvoiceItem.objects.get_or_create(
                    invoice=invoice,
                    product=products[0],
                    defaults={
                        'quantity': 3,
                        'unit_price': Decimal('29.99'),
                        'tax_rate': Decimal('10.00'),
                        'total_price': Decimal('89.97'),
                    }
                )
            elif invoice.invoice_number == 'INV002':
                InvoiceItem.objects.get_or_create(
                    invoice=invoice,
                    product=products[1],
                    defaults={
                        'quantity': 1,
                        'unit_price': Decimal('249.99'),
                        'tax_rate': Decimal('10.00'),
                        'total_price': Decimal('249.99'),
                    }
                )

        self.stdout.write('Created sample invoices and items')

    def create_receipts_and_items(self, suppliers, products):
        """Create sample receipts and receipt items"""
        receipts_data = [
            {
                'receipt_number': 'REC001',
                'supplier': suppliers[0],
                'receipt_date': timezone.now().date(),
                'subtotal': Decimal('465.00'),
                'tax_amount': Decimal('46.50'),
                'total_amount': Decimal('511.50'),
                'status': 'received',
                'is_approved': True,
                'approved_by': User.objects.filter(role='admin').first(),
                'approved_at': timezone.now(),
                'po_number': 'PO001',
                'notes': 'Received all items',
            },
            {
                'receipt_number': 'REC002',
                'supplier': suppliers[1],
                'receipt_date': timezone.now().date(),
                'subtotal': Decimal('240.00'),
                'tax_amount': Decimal('24.00'),
                'total_amount': Decimal('264.00'),
                'status': 'verified',
                'is_approved': True,
                'approved_by': User.objects.filter(role='admin').first(),
                'approved_at': timezone.now(),
                'po_number': 'PO002',
                'notes': 'Verified and approved',
            },
        ]

        manager = User.objects.filter(role='admin').first()
        for receipt_data in receipts_data:
            receipt, created = Receipt.objects.get_or_create(
                receipt_number=receipt_data['receipt_number'],
                defaults={
                    **receipt_data,
                    'created_by': manager,
                }
            )

            # Create receipt items
            if receipt.receipt_number == 'REC001':
                ReceiptItem.objects.get_or_create(
                    receipt=receipt,
                    product=products[0],
                    defaults={
                        'quantity_ordered': 10,
                        'quantity_received': 10,
                        'unit_price': Decimal('15.50'),
                        'tax_rate': Decimal('10.00'),
                        'total_price': Decimal('155.00'),
                        'notes': 'All items received',
                    }
                )
                ReceiptItem.objects.get_or_create(
                    receipt=receipt,
                    product=products[3],
                    defaults={
                        'quantity_ordered': 5,
                        'quantity_received': 5,
                        'unit_price': Decimal('25.00'),
                        'tax_rate': Decimal('10.00'),
                        'total_price': Decimal('125.00'),
                        'notes': 'Good quality',
                    }
                )
            elif receipt.receipt_number == 'REC002':
                ReceiptItem.objects.get_or_create(
                    receipt=receipt,
                    product=products[2],
                    defaults={
                        'quantity_ordered': 20,
                        'quantity_received': 20,
                        'unit_price': Decimal('4.50'),
                        'tax_rate': Decimal('10.00'),
                        'total_price': Decimal('90.00'),
                        'notes': 'Received in good condition',
                    }
                )
                ReceiptItem.objects.get_or_create(
                    receipt=receipt,
                    product=products[1],
                    defaults={
                        'quantity_ordered': 2,
                        'quantity_received': 2,
                        'unit_price': Decimal('120.00'),
                        'tax_rate': Decimal('10.00'),
                        'total_price': Decimal('240.00'),
                        'notes': 'Heavy items, handled carefully',
                    }
                )

        self.stdout.write('Created sample receipts and items')

    def create_debts_and_payments(self):
        """Create sample debts and debt payments"""
        # Get existing invoices that are unpaid
        unpaid_invoices = Invoice.objects.filter(status__in=['issued', 'partially_paid'])

        for invoice in unpaid_invoices:
            debt, created = Debt.objects.get_or_create(
                customer=invoice.customer,
                invoice=invoice,
                defaults={
                    'original_amount': invoice.total_amount,
                    'paid_amount': invoice.paid_amount,
                    'status': 'pending' if invoice.paid_amount == 0 else 'partially_paid',
                    'due_date': invoice.due_date,
                    'created_by': User.objects.filter(role='admin').first(),
                }
            )

            # Create a payment if partially paid
            if invoice.paid_amount > 0:
                DebtPayment.objects.get_or_create(
                    debt=debt,
                    amount=invoice.paid_amount,
                    defaults={
                        'payment_date': timezone.now().date(),
                        'payment_method': 'bank_transfer',
                        'reference_number': f'PAY{debt.id:03d}',
                        'recorded_by': User.objects.filter(role='admin').first(),
                    }
                )

        self.stdout.write('Created sample debts and payments')

    def create_audit_logs(self):
        """Create sample audit logs"""
        users = User.objects.all()
        actions = ['create', 'update', 'view', 'login']
        model_names = ['Product', 'Invoice', 'Supplier', 'Customer']

        for i in range(10):
            AuditLog.objects.create(
                user=random.choice(users) if users else None,
                action=random.choice(actions),
                model_name=random.choice(model_names),
                object_id=random.randint(1, 100),
                object_description=f'Sample {model_names[i % len(model_names)]} {i+1}',
                old_values={'status': 'draft'} if random.choice([True, False]) else {},
                new_values={'status': 'active'} if random.choice([True, False]) else {},
                ip_address=f'192.168.1.{random.randint(1, 255)}',
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            )

        self.stdout.write('Created 10 sample audit logs')

    def create_dashboard_metrics(self):
        """Create dashboard metrics"""
        ManagerDashboardMetrics.objects.get_or_create(
            defaults={
                'total_invoices_issued': Invoice.objects.count(),
                'total_receipts_received': Receipt.objects.count(),
                'total_outstanding_debt': sum(debt.outstanding_amount for debt in Debt.objects.all()),
                'total_overdue_debt': sum(debt.outstanding_amount for debt in Debt.objects.filter(status__in=['pending', 'partially_paid', 'overdue'], due_date__lt=timezone.now().date())),
                'pending_approvals': Invoice.objects.filter(is_approved=False).count() + Receipt.objects.filter(is_approved=False).count(),
                'low_stock_products': Product.objects.filter(quantity_in_stock__lte=10).count(),
                'total_customers': Customer.objects.count(),
                'total_suppliers': Supplier.objects.count(),
            }
        )

        self.stdout.write('Created dashboard metrics')