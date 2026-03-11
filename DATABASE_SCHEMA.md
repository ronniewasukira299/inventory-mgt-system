# Database Schema - Supplier, Inventory, Invoicing & Customer Debt Management System

## System Overview

This document details the comprehensive database schema for the inventory, invoicing, and debt management system. The schema is organized into logical sections covering all aspects of the business operations.

---

## 1. User Management

### accounts.User (extends Django AbstractUser)
- `id` (AutoField, PK)
- `username` (CharField, unique)
- `email` (EmailField, unique)
- `first_name` (CharField)
- `last_name` (CharField)
- `bio` (TextField, nullable)
- `role` (CharField, choices: admin, editor, viewer)
- `joined_date` (DateTimeField, auto_now_add)
- `is_active` (BooleanField)
- `is_staff` (BooleanField)
- `date_joined` (DateTimeField)
- `last_login` (DateTimeField, nullable)

**Relationships:**
- 1:N → Supplier (created_by)
- 1:N → Customer (created_by)
- 1:N → Product (created_by)
- 1:N → Invoice (created_by, approved_by)
- 1:N → Receipt (created_by, approved_by)
- 1:N → Debt (created_by)
- 1:N → DebtPayment (recorded_by)
- 1:N → StockMovement (created_by)
- 1:N → AuditLog (user)

---

## 2. Organization Management

### core.Supplier
- `id` (AutoField, PK)
- `name` (CharField, unique, indexed)
- `contact_person` (CharField)
- `email` (EmailField, unique)
- `phone` (CharField)
- `address` (TextField)
- `city` (CharField)
- `country` (CharField)
- `postal_code` (CharField)
- `rating` (DecimalField, max_digits=3, decimal_places=2)
- `status` (CharField, choices: active, inactive, suspended, default=active, indexed)
- `credit_terms_days` (IntegerField, default=30)
- `notes` (TextField, blank)
- `created_by` (ForeignKey to User, SET_NULL)
- `created_at` (DateTimeField, auto_now_add)
- `updated_at` (DateTimeField, auto_now)

**Indexes:**
- `(status, name)`

### core.Customer
- `id` (AutoField, PK)
- `name` (CharField, unique, indexed)
- `contact_person` (CharField)
- `email` (EmailField, unique)
- `phone` (CharField)
- `address` (TextField)
- `city` (CharField)
- `country` (CharField)
- `postal_code` (CharField)
- `credit_limit` (DecimalField, max_digits=12, decimal_places=2, default=0)
- `credit_used` (DecimalField, max_digits=12, decimal_places=2, default=0)
- `status` (CharField, choices: active, inactive, blocked, default=active, indexed)
- `credit_terms_days` (IntegerField, default=30)
- `notes` (TextField, blank)
- `created_by` (ForeignKey to User, SET_NULL)
- `created_at` (DateTimeField, auto_now_add)
- `updated_at` (DateTimeField, auto_now)

**Computed Properties:**
- `available_credit` = credit_limit - credit_used

**Relationships:**
- 1:N → Invoice
- 1:N → Debt

---

## 3. Inventory Management System

### core.Category
- `id` (AutoField, PK)
- `name` (CharField, unique, indexed)
- `description` (TextField, blank)
- `slug` (SlugField, unique)
- `created_at` (DateTimeField, auto_now_add)
- `updated_at` (DateTimeField, auto_now)

**Meta:**
- Order by: name
- Verbose name plural: Categories

### core.Tag
- `id` (AutoField, PK)
- `name` (CharField, unique)
- `slug` (SlugField, unique)
- `created_at` (DateTimeField, auto_now_add)

**Relationships:**
- M:N ← Product

### core.Product
- `id` (AutoField, PK)
- `code` (CharField, unique, indexed)
- `name` (CharField, indexed)
- `description` (TextField)
- `category` (ForeignKey to Category, CASCADE, indexed)
- `tags` (ManyToManyField to Tag)
- `cost_price` (DecimalField, max_digits=10, decimal_places=2)
- `selling_price` (DecimalField, max_digits=10, decimal_places=2)
- `unit` (CharField, choices: piece, box, kg, liter, meter, default=piece)
- `quantity_in_stock` (IntegerField, default=0)
- `reorder_level` (IntegerField, default=10)
- `reorder_quantity` (IntegerField, default=50)
- `default_supplier` (ForeignKey to Supplier, SET_NULL, nullable)
- `is_active` (BooleanField, default=True)
- `specs` (JSONField, default=dict, blank)
- `created_by` (ForeignKey to User, SET_NULL)
- `created_at` (DateTimeField, auto_now_add)
- `updated_at` (DateTimeField, auto_now)

**Indexes:**
- `code`
- `(category, is_active)`

**Computed Properties:**
- `is_low_stock` = quantity_in_stock <= reorder_level
- `profit_margin` = ((selling_price - cost_price) / selling_price) * 100

### core.Stock
- `id` (AutoField, PK)
- `product` (OneToOneField to Product, CASCADE)
- `quantity` (IntegerField, default=0)
- `location` (CharField, default='Main Warehouse')
- `last_counted_at` (DateTimeField, nullable)
- `updated_at` (DateTimeField, auto_now)

### core.StockMovement
- `id` (AutoField, PK)
- `product` (ForeignKey to Product, CASCADE, indexed)
- `movement_type` (CharField, choices: in, out, adjustment, transfer, return, indexed)
- `quantity` (IntegerField)
- `reference_type` (CharField, max_length=50)
- `reference_id` (IntegerField)
- `notes` (TextField, blank)
- `created_by` (ForeignKey to User, SET_NULL)
- `created_at` (DateTimeField, auto_now_add, indexed)

**Indexes:**
- `(product, created_at)`
- `(movement_type, created_at)`

---

## 4. Invoicing System

### core.Invoice
- `id` (AutoField, PK)
- `invoice_number` (CharField, unique, indexed)
- `customer` (ForeignKey to Customer, PROTECT, indexed)
- `issue_date` (DateField, default=today)
- `due_date` (DateField)
- `subtotal` (DecimalField, max_digits=12, decimal_places=2, default=0)
- `tax_amount` (DecimalField, max_digits=12, decimal_places=2, default=0)
- `total_amount` (DecimalField, max_digits=12, decimal_places=2, default=0)
- `paid_amount` (DecimalField, max_digits=12, decimal_places=2, default=0)
- `status` (CharField, choices: draft, issued, partially_paid, paid, cancelled, overdue, indexed)
- `is_approved` (BooleanField, default=False)
- `approved_by` (ForeignKey to User, SET_NULL, nullable)
- `approved_at` (DateTimeField, nullable)
- `notes` (TextField, blank)
- `created_by` (ForeignKey to User, SET_NULL)
- `created_at` (DateTimeField, auto_now_add)
- `updated_at` (DateTimeField, auto_now)

**Indexes:**
- `(status, -issue_date)`
- `(customer, status)`

**Computed Properties:**
- `outstanding_amount` = total_amount - paid_amount
- `is_overdue` = (today > due_date) AND (status not in ['paid', 'cancelled'])

### core.InvoiceItem
- `id` (AutoField, PK)
- `invoice` (ForeignKey to Invoice, CASCADE)
- `product` (ForeignKey to Product, PROTECT)
- `quantity` (IntegerField)
- `unit_price` (DecimalField, max_digits=10, decimal_places=2)
- `tax_rate` (DecimalField, max_digits=5, decimal_places=2, default=0)
- `total_price` (DecimalField, max_digits=12, decimal_places=2)

---

## 5. Receipting System

### core.Receipt
- `id` (AutoField, PK)
- `receipt_number` (CharField, unique, indexed)
- `supplier` (ForeignKey to Supplier, PROTECT, indexed)
- `receipt_date` (DateField, default=today)
- `subtotal` (DecimalField, max_digits=12, decimal_places=2, default=0)
- `tax_amount` (DecimalField, max_digits=12, decimal_places=2, default=0)
- `total_amount` (DecimalField, max_digits=12, decimal_places=2, default=0)
- `status` (CharField, choices: draft, received, verified, cancelled, indexed)
- `is_approved` (BooleanField, default=False)
- `approved_by` (ForeignKey to User, SET_NULL, nullable)
- `approved_at` (DateTimeField, nullable)
- `po_number` (CharField, blank)
- `notes` (TextField, blank)
- `created_by` (ForeignKey to User, SET_NULL)
- `created_at` (DateTimeField, auto_now_add)
- `updated_at` (DateTimeField, auto_now)

**Indexes:**
- `(status, -receipt_date)`
- `(supplier, status)`

### core.ReceiptItem
- `id` (AutoField, PK)
- `receipt` (ForeignKey to Receipt, CASCADE)
- `product` (ForeignKey to Product, PROTECT)
- `quantity_ordered` (IntegerField)
- `quantity_received` (IntegerField)
- `unit_price` (DecimalField, max_digits=10, decimal_places=2)
- `tax_rate` (DecimalField, max_digits=5, decimal_places=2, default=0)
- `total_price` (DecimalField, max_digits=12, decimal_places=2)
- `notes` (TextField, blank)

---

## 6. Debt Management System

### core.Debt
- `id` (AutoField, PK)
- `customer` (ForeignKey to Customer, CASCADE)
- `invoice` (ForeignKey to Invoice, PROTECT, nullable)
- `original_amount` (DecimalField, max_digits=12, decimal_places=2)
- `paid_amount` (DecimalField, max_digits=12, decimal_places=2, default=0)
- `due_date` (DateField)
- `status` (CharField, choices: pending, partially_paid, paid, overdue, written_off, indexed)
- `reminder_sent_at` (DateTimeField, nullable)
- `last_payment_date` (DateField, nullable)
- `days_overdue` (IntegerField, default=0)
- `collection_attempts` (IntegerField, default=0)
- `notes` (TextField, blank)
- `created_by` (ForeignKey to User, SET_NULL)
- `created_at` (DateTimeField, auto_now_add)
- `updated_at` (DateTimeField, auto_now)

**Indexes:**
- `(customer, status)`
- `(status, due_date)`

**Computed Properties:**
- `outstanding_amount` = original_amount - paid_amount
- `is_overdue` = (today > due_date) AND (status not in ['paid', 'written_off'])

### core.DebtPayment
- `id` (AutoField, PK)
- `debt` (ForeignKey to Debt, CASCADE)
- `amount` (DecimalField, max_digits=12, decimal_places=2)
- `payment_date` (DateField, default=today)
- `payment_method` (CharField, choices: cash, check, bank_transfer, credit_card, other)
- `reference_number` (CharField, blank)
- `notes` (TextField, blank)
- `recorded_by` (ForeignKey to User, SET_NULL)
- `created_at` (DateTimeField, auto_now_add)

---

## 7. Audit & Monitoring

### core.AuditLog
- `id` (AutoField, PK)
- `user` (ForeignKey to User, SET_NULL, nullable, indexed)
- `action` (CharField, choices: create, update, delete, approve, reject, view, export, login, logout, indexed)
- `model_name` (CharField, max_length=100, indexed)
- `object_id` (IntegerField)
- `object_description` (CharField, max_length=255)
- `old_values` (JSONField, default=dict, blank)
- `new_values` (JSONField, default=dict, blank)
- `ip_address` (GenericIPAddressField, nullable)
- `user_agent` (TextField, blank)
- `timestamp` (DateTimeField, auto_now_add, indexed)

**Indexes:**
- `(user, -timestamp)`
- `(model_name, object_id)`

**Meta:**
- Order by: -timestamp
- Immutable (no add/delete/change permissions in admin)

### core.ManagerDashboardMetrics
- `id` (AutoField, PK)
- `total_invoices_issued` (IntegerField, default=0)
- `total_receipts_received` (IntegerField, default=0)
- `total_outstanding_debt` (DecimalField, max_digits=12, decimal_places=2, default=0)
- `total_overdue_debt` (DecimalField, max_digits=12, decimal_places=2, default=0)
- `pending_approvals` (IntegerField, default=0)
- `low_stock_products` (IntegerField, default=0)
- `total_customers` (IntegerField, default=0)
- `total_suppliers` (IntegerField, default=0)
- `last_updated` (DateTimeField, auto_now)

---

## Data Validation Rules

### Product
- cost_price > 0
- selling_price > 0
- quantity_in_stock >= 0
- reorder_level >= 0
- reorder_quantity > 0

### Invoice
- total_amount = subtotal + tax_amount
- paid_amount <= total_amount
- due_date >= issue_date
- can only have items from same customer

### Receipt
- total_amount = subtotal + tax_amount
- quantity_received >= 0
- quantity_received <= quantity_ordered

### Debt
- original_amount > 0
- paid_amount <= original_amount
- outstanding_amount = original_amount - paid_amount
- due_date required

---

## Migration History

| Version | Description |
|---------|-------------|
| 0001_initial | Initial User model and setup |
| 0002_... | Device model and basic setup |
| 0003_managerdashboardmetrics_and_more | Complete system rebuild with new models |

---

## Key Performance Indicators (Derived from Schema)

These metrics can be calculated from the schema:

```
Total Revenue = SUM(Invoice.total_amount WHERE status = 'paid')
Outstanding Revenue = SUM(Invoice.total_amount - Invoice.paid_amount WHERE status IN ['issued', 'partially_paid'])
Total Receivables = SUM(Debt.outstanding_amount WHERE status IN ['pending', 'partially_paid', 'overdue'])
Overdue Receivables = SUM(Debt.outstanding_amount WHERE is_overdue = true)
Inventory Value = SUM(Product.cost_price * Product.quantity_in_stock WHERE is_active = true)
Low Stock Alert = COUNT(Product WHERE quantity_in_stock <= reorder_level AND is_active = true)
Average Collection Period = SUM(Debt.days_overdue) / COUNT(Debt WHERE status != 'paid')
```