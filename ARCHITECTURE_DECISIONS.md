# Architecture Decisions & Design Rationale

## System Overview
This document describes the key architectural decisions made for the Supplier, Inventory, Invoicing & Customer Debt Management System and the rationale behind each choice.

---

## 1. Technology Stack Choices

### Backend: Django 6.0
**Decision:** Use Django 6.0 as the backend framework

**Rationale:**
- Mature, production-proven web framework
- Built-in ORM for database abstraction and query optimization
- Comprehensive admin interface for data management
- Strong security features (CSRF, SQL injection prevention)
- Excellent documentation and large community
- Built-in user authentication system
- Rapid development with batteries included

**Satisfies Requirements:**
- ✓ Real-time monitoring (through dashboard views)
- ✓ Multi-user access control with roles
- ✓ Comprehensive data management

---

## 2. Database Schema Architecture

### Model Organization
**Decision:** Organize models into logical business groupings

**Structure:**
```
Organization Management
├── Supplier
└── Customer

Inventory Management
├── Category
├── Tag
├── Product
├── Stock
└── StockMovement

Invoicing System
├── Invoice
└── InvoiceItem

receipt System
├── Receipt
└── ReceiptItem

Debt Management
├── Debt
└── DebtPayment

Audit & Monitoring
├── AuditLog
└── ManagerDashboardMetrics
```

**Rationale:**
- Mirrors business domain structure
- Improves code maintainability
- Facilitates future modularization
- Clear separation of concerns

### Relationship Design

#### Product Core Relationships
```python
Product (1) ← (Many) InvoiceItem
Product (1) ← (Many) ReceiptItem
Product (1) ← (Many) StockMovement
```

**Decision:** Use `on_delete=models.PROTECT` for financial records

**Rationale:**
```python
class InvoiceItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    # Prevents accidental deletion of products in active invoices
```
- Enforces referential integrity
- Prevents data loss in financial records
- Requires explicit deletion handling
- Audit trail remains intact

**Exception:** Use `on_delete=models.CASCADE` for audit trails
```python
class StockMovement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # Safe to cascade for historical/audit data
```

### Indexing Strategy

**Decision:** Strategic indexing on frequently filtered and sorted fields

**Implemented Indexes:**
```
Invoice: (status, -issue_date) - Dashboard queries
Invoice: (customer, status) - Customer invoice tracking
Debt: (customer, status) - Customer debt tracking
Debt: (status, due_date) - Overdue identification
Product: code - Product lookup
Product: (category, is_active) - Filtered product queries
StockMovement: (product, created_at) - Stock history
```

**Rationale:**
- Improves query performance for common operations
- Enables fast filtering/sorting
- Reduces database load for real-time dashboard
- Worth the write performance trade-off

---

## 3. User Management & Security

### Role-Based Access Control (RBAC)

**Decision:** Use Django's built-in permission system with custom roles

**Roles Defined:**
```python
ROLE_CHOICES = [
    ('admin', 'Admin'),           # Full system access, approvals
    ('editor', 'Editor'),         # Create/edit records, no approval
    ('viewer', 'Viewer'),         # Read-only access
]
```

**Satisfies Proposal Requirement:**
- Manager Dashboard accessible to 'admin' role
- Approval workflows managed by 'admin' users
- Clear visibility control

### Audit Logging

**Decision:** Implement comprehensive, immutable audit trail

**AuditLog Model:**
```python
class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL)
    action = models.CharField(choices=ACTION_CHOICES)
    model_name = models.CharField()  # What was changed
    object_id = models.IntegerField()  # Which record
    object_description = models.CharField()  # Readable name
    old_values = models.JSONField()  # Before state
    new_values = models.JSONField()  # After state
    timestamp = models.DateTimeField(auto_now_add=True)
    # ... plus IP address, user agent
```

**Satisfies Proposal Requirements:**
- ✓ View all transactions (recent_invoices, recent_receipts)
- ✓ See user actions (via AuditLog)
- ✓ Monitor stock movement (via StockMovement + AuditLog)
- ✓ Track changes with before/after values

**Implementation:**
- Signals to auto-log model changes
- Non-editable in Django admin
- Read-only for compliance

---

## 4. Financial Data Management

### Invoice & Receipt Design

**Decision:** Use header + line-items pattern (common in accounting)

**Rationale:**
```python
Invoice Model:
├── Header: invoice#, customer, dates, amounts, status
└── Items (FK relationship):
    ├── Product reference
    ├── Quantity & pricing
    └── Tax details

InvoiceItem Model:
├── Unit-level tracking
├── Individual amounts
└── Allows partial line modifications
```

**Benefits:**
- Normalization reduces redundancy
- Supports partial invoice operations (cancel one item)
- Line-item level auditing
- Flexible for adjustments
- Industry-standard structure

### Amount Calculation

**Decision:** Store both component amounts and calculated totals

**Rationale:**
```python
class Invoice(models.Model):
    subtotal = models.DecimalField()      # Sum of line items
    tax_amount = models.DecimalField()    # Calculated from tax rates
    total_amount = models.DecimalField()  # subtotal + tax_amount
    paid_amount = models.DecimalField()   # Sum of payments
```

**Why Store Both:**
- Total always available (no calculation per request)
- Enables quick aggregation for dashboard
- Historical integrity (calculated values won't change)
- Better for reporting

**Validation:** Application layer ensures:
```
total_amount = subtotal + tax_amount (enforced in save())
paid_amount <= total_amount
```

### Debt Tracking Model

**Decision:** Separate Debt and DebtPayment models

**Rationale:**
```
Debt (1) ← (Many) DebtPayment
```
- Single debt can have multiple payments (partial payments)
- Each payment is immutable historical record
- Enables payment history and aging analysis
- Supports complex collection scenarios

### Approval Workflow

**Decision:** Simple boolean approval system (not complex state machine)

**Current Implementation:**
```python
class Invoice(models.Model):
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, SET_NULL)
    approved_at = models.DateTimeField(null=True)
```

**Satisfies Requirement:** "Approve/reject transactions"

**Future Enhancement Path:**
```
Simple Boolean (now)
    ↓
Multi-level Approval (review → manager approve)
    ↓
Full Workflow Engine (with rejections, comments)
```

---

## 5. Inventory Management System

### Stock Tracking Design

**Decision:** Three-layer tracking:
1. **Current State** (Product.quantity_in_stock)
2. **Status** (Product.reorder_level)
3. **History** (StockMovement audit trail)

**Rationale:**
```python
Product Model:
├── quantity_in_stock: Current balance (updated immediately)
├── reorder_level: Trigger point
└── reorder_quantity: How much to order

StockMovement Model:
├── product: Which product
├── movement_type: in/out/adjustment/transfer/return
├── quantity: Amount moved
├── reference_type: Which created it (receipt, invoice)
├── reference_id: The specific record
└── timestamp: When it happened
```

**Benefits:**
- Dual record: current state + complete history
- Enables stock reconciliation
- Answers "where did this quantity go?"
- Supports analytics and reporting
- Full audit capability

### Reorder Management

**Decision:** Dashboard alerts without automatic POs

**Rationale:**
```python
Product.is_low_stock property:
    return quantity_in_stock <= reorder_level
```
- Displayed on dashboard
- Gives business owner control
- Manual review ensures appropriateness
- Can automate later without schema changes

---

## 6. Dashboard & Real-Time Monitoring

### Real-Time vs. Cached Data

**Decision:** Hybrid approach

**Real-Time Data** (live queries):
```python
context['recent_invoices'] = Invoice.objects.select_related(
    'customer'
).order_by('-created_at')[:5]
# Shows latest transactions immediately
```

**Cached Metrics** (computed periodically):
```python
context['total_outstanding_debt'] = Debt.objects.filter(
    status__in=['pending', 'partially_paid', 'overdue']
).aggregate(total=Sum('original_amount') - Sum('paid_amount'))

# Replaces aggregation with ManagerDashboardMetrics
# Updated hourly or on-demand
```

**Rationale:**
- Recent transactions must be current
- Complex aggregations can be cached
- Balances timeliness with performance
- Easy to implement, future: add Celery for async updates

### Manager Dashboard Features

**Satisfies All "Manager Monitoring" Requirements:**

✓ **View all transactions** → Recent Invoices/Receipts display
✓ **See user actions** → AuditLog admin interface
✓ **Monitor stock movement** → Dashboard low stock alerts + StockMovement audit
✓ **Approve/reject transactions** → Approval workflows on Invoice/Receipt
✓ **View debts and collection periods** → Debt metrics and aging dashboard

**Key Metrics Displayed:**
```python
- Total invoices/receipts
- Outstanding vs. paid amounts
- Overdue debt count
- Days overdue tracking
- Low stock alerts
- Pending approvals count
- Customer/supplier totals
```

---

## 7. API Architecture

### RESTful Design

**Decision:** Follow REST conventions for API endpoints

**Pattern:**
```
GET    /api/invoices/           # List (with pagination)
POST   /api/invoices/           # Create
GET    /api/invoices/{id}/      # Retrieve specific
PUT    /api/invoices/{id}/      # Update
DELETE /api/invoices/{id}/      # Delete (where appropriate)
POST   /api/invoices/{id}/approve/  # Custom action
```

**Used By:**
- JavaScript AJAX calls from frontend
- Future mobile app integration
- Third-party integrations

### API Pagination

**Decision:** Enforce server-side pagination

**Configuration:**
```python
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
```

**Rationale:**
- Prevents full database dump
- Improves response time
- Enables efficient pagination UI
- Client requests specific pages

---

## 8. Security Architecture

### Defense in Depth

**Layer 1 - Framework Level:**
- Django CSRF middleware enabled
- SQL injection prevention through ORM
- XSS protection in templates
- HTTPS enforcement in production

**Layer 2 - Application Level:**
- Role-based access control
- Login required on sensitive views
- Audit logging of all changes

**Layer 3 - Data Level:**
- Foreign key constraints
- Data validation on save()
- Immutable audit trail

### No Payment Processing

**Decision:** Record payment method but don't process card data

**Rationale:**
```python
class DebtPayment(models.Model):
    payment_method = choices: [cash, check, bank_transfer, credit_card]
    # Records HOW payment came in, not card numbers
    reference_number = models.CharField()  # Check #, txn ID, etc.
```

- No PCI compliance burden initially
- Payment processor integration point clear
- Reference numbers enable reconciliation
- Can integrate Stripe/Square later

---

## 9. Error Handling & Validation

### Business Logic Validation

**Decision:** Implement at model level with custom validators

**Examples:**
```python
class Invoice(models.Model):
    def clean(self):
        if self.total_amount != self.subtotal + self.tax_amount:
            raise ValidationError("Amount mismatch")
        if self.due_date < self.issue_date:
            raise ValidationError("Due date before issue date")

class Debt(models.Model):
    def clean(self):
        if self.paid_amount > self.original_amount:
            raise ValidationError("Paid amount exceeds original")
```

**Rationale:**
- Business rules enforced consistently
- Work in forms, API, admin
- Tests can verify validation

---

## 10. Deployment Architecture

### Local Development
```
SQLite Database
├── No setup required
└── Good for testing

Docker Compose (Optional)
├── PostgreSQL service
└── Matches production closer
```

### Production
```
PostgreSQL 15
├── Reliable, mature database
├── Better concurrency handling
└── Supports advanced features

Django Application
├── Gunicorn WSGI server
├── Environment-based config
└── Separate settings

Static Files
├── AWS S3 or local storage
└── Serves CSS/JS/images
```

### Configuration Management

**Decision:** Environment variables for all sensitive config

**Categories:**
- Database credentials
- Secret key
- Debug mode
- ALLOWED_HOSTS
- Email settings
- Payment processor keys

---

## 11. Data Migration Path

### From Old System

**Decision:** Implement data importers as management commands

**Rationale:**
```python
# core/management/commands/import_old_devices.py
class Command(BaseCommand):
    def handle(self, *args, **options):
        # Read from old system
        # Map to new models
        # Validate data
        # Bulk create or upsert
```

**Benefits:**
- Reusable and testable
- Can run multiple times safely
- Auditable process
- Easy to debug and modify

---

## 12. Performance Optimization

### Query Optimization

**Decision:** Use select_related() and prefetch_related() consistently

**Pattern:**
```python
# Dashboard view
invoices = Invoice.objects.select_related(
    'customer', 'created_by'
).prefetch_related(
    'items__product'
).filter(
    status='paid'
)[::5]  # Recent 5

# Advantages:
# - select_related: Reduces queries for FK relationships
# - prefetch_related: Optimizes reverse FK lookups
# - Result: 1 query instead of N+1
```

### Database Indexes (Covered Above)

### Pagination (Covered Above)

### Caching Strategy

**Layers:**
1. **Database Indexes** - Query-level optimization
2. **Model Aggregations** - `ManagerDashboardMetrics` updated hourly
3. **HTTP Caching** - `Cache-Control` headers on static files
4. **Future:** Redis for session/object caching

---

## 13. Testing Strategy

### Test Organization
```
core/
├── tests/
│   ├── __init__.py
│   ├── test_models.py         # Model business logic
│   ├── test_views.py          # View permissions & context
│   ├── test_forms.py          # Form validation
│   └── test_api.py            # API endpoints
```

### Coverage Goals
- **Models:** 100% (business logic)
- **Views:** 80% (happy paths + errors)
- **Forms:** 80% (validation rules)
- **Utilities:** 100% (helper functions)

---

## 14. Documentation Strategy

### Code Documentation
- Docstrings on all classes and complex methods
- README with quick start
- DATABASE_SCHEMA.md for ER diagrams
- API_DOCUMENTATION.md with endpoint details

### User Documentation
- Admin interface help texts
- Dashboard tooltips
- User manual (future)

---

## Related Decisions

| Topic | Document |
|-------|----------|
| Database Schema | [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) |
| API Specs | [API_DOCUMENTATION.md](API_DOCUMENTATION.md) |
| Project Structure | [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) |
| Contributing | [CONTRIBUTING.md](CONTRIBUTING.md) |

---

## Decision Log

| Date | Decision | Status |
|------|----------|--------|
| 2024-03-01 | Django 6.0 backend | ✓ Implemented |
| 2024-03-01 | Role-based access control | ✓ Implemented |
| 2024-03-01 | Separate Invoice/Item models | ✓ Implemented |
| 2024-03-01 | Immutable audit trail | ✓ Implemented |
| 2024-03-01 | Hybrid real-time/cached dashboard | ✓ Implemented |
| 2024-03-01 | REST API design | ✓ Implemented |
| 2024-03-01 | StockMovement audit trail | ✓ Implemented | 
| Future | Celery for async tasks | Not started |
| Future | Redis for caching | Not started |
| Future | Advanced approval workflow | Not started |
| Future | Mobile app | Not started |

---

## Conclusion

This architecture provides:
- ✓ Scalability (database indexes, pagination, caching)
- ✓ Security (audit trail, RBAC, validation)
- ✓ Maintainability (clear structure, documentation)
- ✓ Flexibility (easy to extend)
- ✓ Performance (optimized queries, caching)

All proposal requirements are satisfied with room for future enhancements.
