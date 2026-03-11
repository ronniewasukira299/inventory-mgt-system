# Project Structure - Supplier, Inventory, Invoicing & Debt Management System

## Directory Tree
```
inventory-mgt-system/
│
├── accounts/                           # User authentication & management
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 000_initial.py
│   ├── __init__.py
│   ├── admin.py                        # User admin configuration
│   ├── apps.py
│   ├── forms.py                        # Login, registration, password reset
│   ├── models.py                       # Custom User with roles (admin, editor, viewer)
│   ├── tests.py                        # Authentication tests
│   ├── urls.py                         # Auth URL patterns
│   ├── views.py                        # Login, logout, register, profile
│   └── templates/accounts/
│       ├── login.html
│       ├── register.html
│       ├── password_reset.html
│       └── profile.html
│
├── core/                               # Main business logic
│   ├── management/
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── seed_devices.py         # Sample data loading
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   ├── 0002_alter_device_*.py
│   │   └── 0003_managerdashboardmetrics*.py
│   ├── __init__.py
│   ├── admin.py                        # Django admin configuration
│   │                                    # - SupplierAdmin
│   │                                    # - CustomerAdmin
│   │                                    # - ProductAdmin
│   │                                    # - StockAdmin
│   │                                    # - InvoiceAdmin (with inline items)
│   │                                    # - ReceiptAdmin (with inline items)
│   │                                    # - DebtAdmin (with inline payments)
│   │                                    # - AuditLogAdmin (read-only)
│   │
│   ├── apps.py                         # App configuration
│   ├── context_processors.py           # Template context helpers
│   ├── forms.py                        # Business forms
│   │                                    # - ProductSearchForm
│   │                                    # - InvoiceForm
│   │                                    # - ReceiptForm
│   │                                    # - CustomerForm
│   │                                    # - SupplierForm
│   │                                    # - DebtPaymentForm
│   │
│   ├── models.py                       # All business models (400+ lines)
│   │                                    # ├── Supplier
│   │                                    # ├── Customer
│   │                                    # ├── Category
│   │                                    # ├── Tag
│   │                                    # ├── Product
│   │                                    # ├── Stock
│   │                                    # ├── StockMovement
│   │                                    # ├── Invoice
│   │                                    # ├── InvoiceItem
│   │                                    # ├── Receipt
│   │                                    # ├── ReceiptItem
│   │                                    # ├── Debt
│   │                                    # ├── DebtPayment
│   │                                    # ├── AuditLog
│   │                                    # └── ManagerDashboardMetrics
│   │
│   ├── tests.py                        # Model and view tests
│   ├── urls.py                         # Core URL patterns
│   │                                    # ├── /                    → ProductListView
│   │                                    # ├── /device/<id>/        → ProductDetailView
│   │                                    # ├── /dashboard/          → ManagerDashboardView
│   │                                    # └── /contact/            → contact_view
│   │
│   ├── views.py                        # Business logic views
│   │                                    # ├── ProductListView
│   │                                    # ├── ProductDetailView
│   │                                    # ├── ManagerDashboardView (main feature)
│   │                                    # └── contact_view
│   │
│   └── templates/core/
│       ├── contact.html
│       ├── device_comparison.html      # Deprecated (redirects to dashboard)
│       ├── device_detail.html          # Product detail
│       ├── device_list.html            # Product list
│       └── manager_dashboard.html      # Real-time monitoring dashboard ★
│
├── api/                                # REST API endpoints
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py                        # API endpoint tests
│   ├── urls.py                         # API URL patterns
│   │                                    # ├── /api/devices/      → device_list_api
│   │                                    # └── /api/search/       → device_search_api
│   │
│   ├── views.py                        # API view functions
│   │                                    # ├── device_list_api()
│   │                                    # └── device_search_api()
│   │
│   └── migrations/
│       └── __init__.py
│
├── blog/                               # Blog functionality (future)
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                       # Blog models (not implemented)
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── templates/blog/
│
├── content/                            # Static content management (future)
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── templates/content/
│
├── notifications/                      # Notification system (future)
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── templates/notifications/
│
├── inventory_mgt/                      # Project settings & config
│   ├── __init__.py
│   ├── asgi.py                         # ASGI configuration
│   ├── settings.py                     # Django settings
│   │                                    # ├── INSTALLED_APPS
│   │                                    # ├── MIDDLEWARE
│   │                                    # ├── Database config
│   │                                    # ├── Auth config
│   │                                    # └── Static files config
│   │
│   ├── urls.py                         # Main URL routing
│   │                                    # ├── admin/
│   │                                    # ├── accounts/
│   │                                    # ├── api/
│   │                                    # ├── core/
│   │                                    # └── static/
│   │
│   └── wsgi.py                         # WSGI configuration
│
├── templates/                          # Global templates
│   ├── base.html                       # Base template with nav/footer
│   ├── 404.html                        # Error pages
│   ├── 500.html
│   ├── accounts/                       # Auth templates
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── password_reset.html
│   │   └── profile.html
│   │
│   └── core/                           # Business templates
│       ├── contact.html
│       ├── device_detail.html
│       ├── device_list.html
│       └── manager_dashboard.html      # ★ Main dashboard
│
├── static/                             # Static files (JavaScript, CSS, images)
│   ├── css/
│   │   ├── base.css                    # Global styles
│   │   ├── dashboard.css               # Dashboard styles
│   │   └── bootstrap-custom.css        # Bootstrap customization
│   │
│   ├── js/
│   │   ├── base.js                     # Global JavaScript
│   │   ├── dashboard.js                # Dashboard interactions
│   │   └── api-client.js               # API helpers
│   │
│   └── images/
│       ├── logo.png
│       └── icons/
│
├── db.sqlite3                          # SQLite database (development)
├── manage.py                           # Django management script
│
├── requirements.txt                    # Python dependencies
│                                       # ├── Django==6.0
│                                       # ├── djangorestframework
│                                       # ├── django-cors-headers
│                                       # ├── python-decouple (for env vars)
│                                       # └── psycopg2 (PostgreSQL driver)
│
├── Dockerfile                          # Docker image definition
├── docker-compose.yml                  # Docker Compose configuration
│
├── .env.example                        # Environment variables template
├── .gitignore                          # Git ignore rules
│
├── README.md                           # Project overview
├── API_DOCUMENTATION.md                # ★ API reference
├── DATABASE_SCHEMA.md                  # ★ Database schema & ER diagrams
├── ARCHITECTURE_DECISIONS.md           # ★ Design rationale
├── PROJECT_STRUCTURE.md                # This file
└── CONTRIBUTING.md                     # Contribution guidelines
```

---

## App Responsibilities

### accounts/
**Purpose:** User authentication and management

**Key Components:**
- **models.py**
  - Custom `User` model extending `AbstractUser`
  - Fields: `role`, `bio`, `joined_date`
  - Roles: admin, editor, viewer

- **views.py**
  - Login view with CSRF protection
  - Registration with validation
  - Password reset workflow
  - User profile management

- **forms.py**
  - AuthenticationForm customization
  - UserCreationForm customization
  - PasswordResetForm

- **admin.py**
  - UserAdmin with role management
  - User listing and filtering

**Responsibilities:**
- ✓ User registration and login
- ✓ Password management
- ✓ Permission/role assignment
- ✓ User profile management

---

### core/
**Purpose:** Core business logic and data models

**Key Components:**

#### models.py (15+ models, 400+ lines)
```python
# Organization Models
- Supplier
- Customer

# Inventory Models
- Category
- Tag
- Product
- Stock
- StockMovement

# Financial Models
- Invoice + InvoiceItem
- Receipt + ReceiptItem
- Debt + DebtPayment

# System Models
- AuditLog
- ManagerDashboardMetrics
```

#### views.py (Primary Features)
- **ProductListView** - List/search products
- **ProductDetailView** - Product details
- **ManagerDashboardView** ★ - Real-time dashboard
- **contact_view** - Contact form

#### admin.py (100+ lines)
- Configured admin interface for all 15+ models
- Inline editing for related items
- Filtered lists and search
- Read-only views for audit logs
- Color-coded status indicators

#### urls.py
```
''               → ProductListView
'device/<id>/'   → ProductDetailView
'dashboard/'     → ManagerDashboardView ★
'contact/'       → contact_view
```

#### forms.py
- ProductSearchForm - Search and filter products
- InvoiceForm - Create invoices
- ReceiptForm - Record receipts
- CustomerForm - Manage customers
- SupplierForm - Manage suppliers
- DebtPaymentForm - Record payments

**Responsibilities:**
- ✓ All business data models
- ✓ Admin interface for all entities
- ✓ Core views and forms
- ✓ Dashboard view

---

### api/
**Purpose:** RESTful API endpoints for programmatic access

**Components:**
- **views.py**
  - `device_list_api()` - List products (backward compatible)
  - `device_search_api()` - Search products

- **urls.py**
  - `/api/devices/` → device_list_api
  - `/api/search/` → device_search_api

**Future Enhancement:**
- Serializers for all models
- ViewSets for admin operations
- Filtering, pagination
- Complex report endpoints

**Responsibilities:**
- ✓ JSON API endpoints
- ✓ Mobile app support (future)
- ✓ Third-party integrations

---

### accounts/, blog/, content/, notifications/
**Status:** ✓ Structured, some features not yet implemented

- **accounts/**: ✓ Complete with custom user roles
- **blog/**: Placeholder for blog functionality
- **content/**: Placeholder for content management
- **notifications/**: Placeholder for notification system

---

## Key Models Relationship Diagram

```
User ←── (1:N) ──→ Supplier
User ←── (1:N) ──→ Customer
User ←── (1:N) ──→ Product
User ←── (1:N) ──→ Invoice
User ←── (1:N) ──→ Receipt
User ←── (1:N) ──→ Debt
User ←── (1:N) ──→ AuditLog

Category ←─ (1:N) ──→ Product
Tag ←───── (M:N) ──→ Product
Supplier ← (1:N) ──→ Receipt
Customer ← (1:N) ──→ Invoice
Customer ← (1:N) ──→ Debt

Invoice ── (1:N) ──→ InvoiceItem
Invoice ── (1:N) ──→ Debt
InvoiceItem ← (1:N) ──→ Product

Receipt ─── (1:N) ──→ ReceiptItem
ReceiptItem ← (1:N) ──→ Product

Debt ────── (1:N) ──→ DebtPayment

Product ── (1:N) ──→ StockMovement
Product ── (1:1) ──→ Stock
```

---

## Template Hierarchy

```
base.html (Global wrapper)
├── navbar (includes nav items)
├── breadcrumb (current location)
├── messages (Django messages)
├── {% block content %}
├── footer
└── scripts

Extends:
├── accounts/login.html
├── accounts/register.html
├── accounts/profile.html
├── core/device_list.html
├── core/device_detail.html
├── core/manager_dashboard.html ★
└── core/contact.html
```

---

## URL Routing

```
/ (project root, urls.py)
├── admin/                      → Django admin
├── accounts/
│   ├── login/
│   ├── register/
│   ├── password_reset/
│   └── profile/
├── api/
│   ├── devices/
│   └── search/
└── core/
    ├── (product list)
    ├── device/<id>/            (product detail)
    ├── dashboard/              ★ Manager dashboard
    └── contact/
```

---

## Database Structure

**Tables:**
- auth_user (Django default)
- accounts_user (custom User model)
- core_category
- core_tag
- core_product
- core_product_tags (M2M join table)
- core_stock
- core_stockmovement
- core_supplier
- core_customer
- core_invoice
- core_invoiceitem
- core_receipt
- core_receiptitem
- core_debt
- core_debtpayment
- core_auditlog
- core_managerdashboardmetrics

**Total:** ~18 core tables + Django admin tables

---

## Configuration Files

### settings.py
**Key Settings:**
- DEBUG = True (development)
- DATABASE: SQLite (dev) or PostgreSQL (prod)
- INSTALLED_APPS: 9 apps
- MIDDLEWARE: CORS, CSRF, Auth, Security
- Templates: /templates directory
- Static: /static directory
- Auth: Custom User model

### urls.py
**Route Configuration:**
- Admin interface
- App URLs (accounts, core, api)
- Static file serving (development)

### wsgi.py & asgi.py
- WSGI for production (Gunicorn)
- ASGI for async operations (future)

---

## File Size Reference

| File | Lines | Purpose |
|------|-------|---------|
| core/models.py | 400+ | All business models |
| core/admin.py | 250+ | Admin configuration |
| core/views.py | 150+ | Business views |
| core/forms.py | 100+ | Form definitions |
| accounts/models.py | 20 | Custom User |
| templates/core/manager_dashboard.html | 200+ | Dashboard UI ★ |
| DATABASE_SCHEMA.md | 300+ | Schema docs |

---

## Development Workflow

1. **Models** → Update core/models.py
2. **Migrations** → `python manage.py makemigrations`
3. **Admin** → Register in core/admin.py
4. **Forms** → Create in core/forms.py
5. **Views** → Implement in core/views.py
6. **Templates** → Create in templates/core/
7. **Tests** → Add to core/tests.py
8. **URLs** → Add to core/urls.py

---

## Future Enhancements

| Component | Status | Notes |
|-----------|--------|-------|
| Blog app | Planned | Post, Comment, Category models |
| Notifications | Planned | Email alerts for overdue debt |
| Reports | Planned | PDF export, scheduled reports |
| Mobile App | Planned | Uses API endpoints |
| Advanced Dashboard | Planned | Charts, graphs, real-time updates |
| Celery Tasks | Planned | Async processing |
| Redis Caching | Planned | Performance optimization |

---

## Deployment Considerations

- **Development:** `python manage.py runserver`
- **Production:** Gunicorn + Nginx + PostgreSQL + Docker
- **Static Files:** Django staticfiles in dev, S3 in prod
- **Backups:** PostgreSQL dumps daily
- **Monitoring:** Django logs + Sentry error tracking

---

## Contributing Guidelines

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Branch naming conventions
- Code style (PEP 8)
- Testing requirements
- Pull request process

