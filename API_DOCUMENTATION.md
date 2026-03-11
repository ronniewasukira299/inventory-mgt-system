# API Documentation - Inventory & Invoicing System

## Base URL
```
http://localhost:8000/api/
```

## Authentication
All API endpoints require authentication using token-based authentication. Include your authentication token in the Authorization header:
```
Authorization: Token <your-token>
```

## Response Format
All responses are returned as JSON with standard HTTP status codes.

---

## Endpoints

### 1. Products API

#### List Products
- **URL:** `/api/products/`
- **Method:** `GET`
- **Query Parameters:**
  - `category` (optional): Filter by category ID
  - `is_active` (optional): Filter by active status
  - `search` (optional): Search in name and code
  - `page` (optional): Page number

**Example Request:**
```
GET /api/products/?category=1&is_active=true
```

**Response (200):**
```json
{
  "count": 50,
  "results": [
    {
      "id": 1,
      "code": "PROD001",
      "name": "Product Name",
      "category": 1,
      "cost_price": "10.00",
      "selling_price": "15.00",
      "quantity_in_stock": 100,
      "is_active": true,
      "created_at": "2024-03-01T10:30:00Z"
    }
  ]
}
```

#### Product Search
- **URL:** `/api/search/`
- **Method:** `GET`
- **Parameters:**
  - `q` (required): Search query string

**Example Request:**
```
GET /api/search/?q=Arduino
```

**Response (200):**
```json
{
  "suggestions": [
    {"id": 1, "code": "PROD001", "name": "Arduino Uno"},
    {"id": 3, "code": "PROD003", "name": "Arduino Mega"}
  ]
}
```

### 2. Invoicing API

#### List Invoices
- **URL:** `/api/invoices/`
- **Method:** `GET`
- **Filters:**
  - `customer`: Customer ID
  - `status`: Invoice status (draft, issued, partially_paid, paid, overdue)
  - `from_date`: Start date (YYYY-MM-DD)
  - `to_date`: End date (YYYY-MM-DD)

#### Create Invoice
- **URL:** `/api/invoices/`
- **Method:** `POST`

**Request Body:**
```json
{
  "invoice_number": "INV-2024-001",
  "customer": 1,
  "issue_date": "2024-03-10",
  "due_date": "2024-04-10",
  "items": [
    {
      "product": 1,
      "quantity": 5,
      "unit_price": "100.00",
      "tax_rate": "10.00"
    }
  ]
}
```

**Response (201):**
```json
{
  "id": 1,
  "invoice_number": "INV-2024-001",
  "customer": 1,
  "total_amount": "550.00",
  "status": "draft",
  "created_at": "2024-03-01T10:30:00Z"
}
```

#### Get Invoice Details
- **URL:** `/api/invoices/{id}/`
- **Method:** `GET`

**Response (200):**
```json
{
  "id": 1,
  "invoice_number": "INV-2024-001",
  "customer": { "id": 1, "name": "Customer Name" },
  "issue_date": "2024-03-10",
  "due_date": "2024-04-10",
  "subtotal": "500.00",
  "tax_amount": "50.00",
  "total_amount": "550.00",
  "paid_amount": "0.00",
  "outstanding_amount": "550.00",
  "status": "issued",
  "is_approved": true,
  "items": [
    {
      "id": 1,
      "product": { "id": 1, "name": "Product Name" },
      "quantity": 5,
      "unit_price": "100.00",
      "tax_rate": "10.00",
      "total_price": "550.00"
    }
  ]
}
```

#### Approve Invoice
- **URL:** `/api/invoices/{id}/approve/`
- **Method:** `POST`

### 3. Receipts API

#### List Receipts
- **URL:** `/api/receipts/`
- **Method:** `GET`
- **Filters:**
  - `supplier`: Supplier ID
  - `status`: Receipt status

#### Create Receipt
- **URL:** `/api/receipts/`
- **Method:** `POST`

**Request Body:**
```json
{
  "receipt_number": "RCP-2024-001",
  "supplier": 1,
  "receipt_date": "2024-03-10",
  "po_number": "PO-2024-001",
  "items": [
    {
      "product": 1,
      "quantity_ordered": 100,
      "quantity_received": 100,
      "unit_price": "10.00",
      "tax_rate": "5.00"
    }
  ]
}
```

### 4. Customer Management API

#### List Customers
- **URL:** `/api/customers/`
- **Method:** `GET`
- **Filters:**
  - `status`: active, inactive, blocked
  - `search`: Search by name or email

#### Get Customer Details
- **URL:** `/api/customers/{id}/`
- **Method:** `GET`

**Response includes:**
- Customer information
- Credit information (limit, used, available)
- Recent invoices
- Outstanding debts

#### Create Customer
- **URL:** `/api/customers/`
- **Method:** `POST`

**Request Body:**
```json
{
  "name": "New Customer",
  "contact_person": "John Doe",
  "email": "john@example.com",
  "phone": "1234567890",
  "address": "123 Main St",
  "city": "City",
  "country": "Country",
  "postal_code": "12345",
  "credit_limit": "10000.00",
  "credit_terms_days": 30,
  "status": "active"
}
```

### 5. Suppliers API

#### List Suppliers
- **URL:** `/api/suppliers/`
- **Method:** `GET`
- **Filters:**
  - `status`: active, inactive, suspended
  - `search`: Search by name

#### Get Supplier Details
- **URL:** `/api/suppliers/{id}/`
- **Method:** `GET`

#### Create Supplier
- **URL:** `/api/suppliers/`
- **Method:** `POST`

### 6. Debt Management API

#### List Debts
- **URL:** `/api/debts/`
- **Method:** `GET`
- **Filters:**
  - `customer`: Customer ID
  - `status`: pending, partially_paid, paid, overdue, written_off
  - `overdue_only`: true/false

#### Get Debt Details
- **URL:** `/api/debts/{id}/`
- **Method:** `GET`

**Response:**
```json
{
  "id": 1,
  "customer": { "id": 1, "name": "Customer Name" },
  "invoice": { "id": 1, "invoice_number": "INV-2024-001" },
  "original_amount": "1000.00",
  "paid_amount": "300.00",
  "outstanding_amount": "700.00",
  "due_date": "2024-04-10",
  "status": "partially_paid",
  "days_overdue": 5,
  "collection_attempts": 2,
  "is_overdue": true,
  "payments": [
    {
      "id": 1,
      "amount": "300.00",
      "payment_date": "2024-03-15",
      "payment_method": "bank_transfer",
      "reference_number": "TXN-001"
    }
  ]
}
```

#### Record Debt Payment
- **URL:** `/api/debts/{id}/record_payment/`
- **Method:** `POST`

**Request Body:**
```json
{
  "amount": "500.00",
  "payment_date": "2024-03-10",
  "payment_method": "bank_transfer",
  "reference_number": "TXN-123456",
  "notes": "Payment for invoice INV-2024-001"
}
```

**Response (200):**
```json
{
  "id": 1,
  "status": "success",
  "message": "Payment recorded successfully",
  "debt": {
    "id": 1,
    "outstanding_amount": "200.00",
    "status": "partially_paid"
  }
}
```

### 7. Reports API

#### Sales Report
- **URL:** `/api/reports/sales/`
- **Method:** `GET`
- **Parameters:**
  - `from_date` (required): Start date
  - `to_date` (required): End date

**Response:**
```json
{
  "period": { "from_date": "2024-01-01", "to_date": "2024-03-31" },
  "totals": {
    "total_invoices": 150,
    "total_revenue": "50000.00",
    "total_paid": "40000.00",
    "total_outstanding": "10000.00"
  }
}
```

#### Inventory Status
- **URL:** `/api/reports/inventory/`
- **Method:** `GET`

**Response:**
```json
{
  "summary": {
    "total_products": 500,
    "total_value": "250000.00",
    "low_stock_count": 25
  },
  "low_stock_items": [...]
}
```

#### Debt Aging Report
- **URL:** `/api/reports/debt-aging/`
- **Method:** `GET`

**Response:**
```json
{
  "summary": {
    "total_outstanding": "100000.00",
    "total_overdue": "35000.00"
  },
  "by_age": {
    "current": "40000.00",
    "30_days": "30000.00",
    "60_days": "20000.00",
    "90_plus_days": "10000.00"
  }
}
```

### 8. Dashboard API

#### Metrics
- **URL:** `/api/dashboard/metrics/`
- **Method:** `GET`

**Response:**
```json
{
  "invoices": {
    "total": 150,
    "pending_approval": 5,
    "overdue": 3
  },
  "debts": {
    "total_outstanding": "100000.00",
    "overdue": "35000.00"
  },
  "inventory": {
    "low_stock_items": 25,
    "total_value": "250000.00"
  },
  "approvals_pending": 7
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request",
  "errors": { "field_name": ["Error message"] }
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created
- `204 No Content` - Request successful, no content to return
- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Pagination

Use `page` and `page_size` query parameters:
```
GET /api/products/?page=2&page_size=50
```

---

## Filtering & Searching

Use query parameters to filter:
```
GET /api/invoices/?status=paid&customer=1
GET /api/customers/?search=john&status=active
```

---

## Examples

Get all devices (for backward compatibility):
```bash
GET /api/products/
```

Search products:
```bash
curl -X GET "http://localhost:8000/api/search/?q=Arduino" \
  -H "Authorization: Token YOUR_TOKEN"
```

Create invoice:
```bash
curl -X POST http://localhost:8000/api/invoices/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "invoice_number": "INV-2024-001",
    "customer": 1,
    "issue_date": "2024-03-10",
    "due_date": "2024-04-10"
  }'
```

**Example Request:**
- `/api/search/?q=arduino` - Search for devices containing "arduino"

## Views

### Device List View
- **URL**: `/`
- **Template**: core/device_list.html
- **Context Variables**:
  - `devices` (Page object): Paginated list of devices
  - `form` (DeviceSearchForm): Search form with fields for search, category, and device_type
  - `categories` (QuerySet): All available categories
  - `page_obj`: Pagination object
  - `is_paginated` (Boolean): Whether results are paginated

### Device Detail View
- **URL**: `/device/<id>/`
- **Template**: core/device_detail.html
- **Required**: User must be authenticated
- **Context Variables**:
  - `device` (Device object): The device being viewed
  - `user` (User object): Current authenticated user

### Device Comparison View
- **URL**: `/compare/<id1>/<id2>/`
- **Template**: core/device_comparison.html
- **Required**: User must be authenticated
- **Context Variables**:
  - `device1` (Device object): First device
  - `device2` (Device object): Second device
  - `comparison` (DeviceComparison object): Comparison data

### Contact View
- **URL**: `/contact/`
- **Template**: core/contact.html
- **Context Variables**:
  - `form` (ContactForm): Contact form with fields for name, email, subject, message

## Authentication Views

### Login
- **URL**: `/accounts/login/`
- **Method**: GET, POST
- **Template**: accounts/login.html
- **Rate Limit**: 5 attempts per minute (IP-based)
- **Context Variables**:
  - `form` (AuthenticationForm): Login form

### Register
- **URL**: `/accounts/register/`
- **Method**: GET, POST
- **Template**: accounts/register.html
- **Rate Limit**: 3 attempts per minute (IP-based)
- **Context Variables**:
  - `form` (UserRegisterForm): Registration form

### Profile
- **URL**: `/accounts/profile/`
- **Method**: GET
- **Template**: accounts/profile.html
- **Required**: User must be authenticated
- **Context Variables**:
  - `user` (User object): Current user with all profile information

### Password Reset
- **URL**: `/accounts/password_reset/`
- **Method**: GET, POST
- **Template**: accounts/password_reset.html
- **Context Variables**:
  - `form` (PasswordResetForm): Password reset form

### Logout
- **URL**: `/accounts/logout/`
- **Method**: POST
- **Redirects**: To `/accounts/login/`

## Error Responses

### 404 Not Found
Returned when a device or resource does not exist.

### 403 Forbidden
Returned when user lacks necessary permissions.

### 429 Too Many Requests
Returned when rate limit is exceeded (authentication endpoints).

## Search Query Examples

- Search for devices: `GET /?search=arduino`
- Filter by type: `GET /?device_type=serial`
- Filter by category: `GET /?category=1`
- Combine filters: `GET /?search=arduino&device_type=serial`

## Pagination

Device list view returns 10 items per page. Navigate using:
- Current page: `?page=1`
- Next page: `?page=2`
- Previous page: Navigation controls in template

## Rate Limiting

- Login endpoint: 5 attempts per minute per IP
- Register endpoint: 3 attempts per minute per IP
- All other endpoints: No rate limit (except via middleware)