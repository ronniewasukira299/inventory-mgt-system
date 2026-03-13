# MODELS REFERENCE

This document provides plain English descriptions of every field in all models in the inventory management system.

## User Model (accounts/models.py)

- **username**: Unique username for login
- **first_name**: User's first name
- **last_name**: User's last name
- **email**: User's email address (must be unique)
- **password**: Hashed password for authentication
- **bio**: Optional text field for user biography
- **role**: User role with choices: admin, editor, or viewer
- **joined_date**: Date and time when user account was created
- **is_staff**: Boolean indicating if user can access admin interface
- **is_superuser**: Boolean indicating if user has all permissions
- **is_active**: Boolean indicating if account is active
- **date_joined**: Date and time when user joined (auto-set)
- **last_login**: Date and time of last login

## Supplier Model (core/models.py)

- **name**: Supplier company name (must be unique)
- **contact_person**: Name of the main contact person
- **email**: Supplier's email address (must be unique)
- **phone**: Supplier's phone number
- **address**: Supplier's street address
- **city**: City where supplier is located
- **country**: Country where supplier is located
- **postal_code**: Postal/ZIP code
- **rating**: Supplier rating from 0.00 to 5.00 (2 decimal places)
- **status**: Supplier status: active, inactive, or suspended
- **credit_terms_days**: Number of days for payment terms (default 30)
- **notes**: Additional notes about the supplier
- **created_by**: User who created this supplier record
- **created_at**: Date and time when record was created
- **updated_at**: Date and time when record was last updated

## Customer Model (core/models.py)

- **name**: Customer company name (must be unique)
- **contact_person**: Name of the main contact person
- **email**: Customer's email address (must be unique)
- **phone**: Customer's phone number
- **address**: Customer's street address
- **city**: City where customer is located
- **country**: Country where customer is located
- **postal_code**: Postal/ZIP code
- **credit_limit**: Maximum amount customer can owe (12 digits, 2 decimals)
- **credit_used**: Current amount customer owes (12 digits, 2 decimals)
- **status**: Customer status: active, inactive, or blocked
- **credit_terms_days**: Number of days for payment terms (default 30)
- **notes**: Additional notes about the customer
- **created_by**: User who created this customer record
- **created_at**: Date and time when record was created
- **updated_at**: Date and time when record was last updated

## Category Model (core/models.py)

- **name**: Category name (must be unique)
- **description**: Description of what this category contains
- **slug**: URL-friendly version of the name (must be unique)
- **created_at**: Date and time when category was created
- **updated_at**: Date and time when category was last updated

## Tag Model (core/models.py)

- **name**: Tag name (must be unique)
- **slug**: URL-friendly version of the name (must be unique)
- **created_at**: Date and time when tag was created

## Product Model (core/models.py)

- **code**: Unique product code/SKU
- **name**: Product name
- **description**: Detailed product description
- **category**: Category this product belongs to
- **tags**: Many-to-many relationship with Tag model
- **cost_price**: Price paid to supplier (10 digits, 2 decimals)
- **selling_price**: Price sold to customers (10 digits, 2 decimals)
- **unit**: Unit of measurement: piece, box, kg, liter, meter, carton, or bag
- **quantity_in_stock**: Current quantity available
- **reorder_level**: Minimum quantity before reorder is needed
- **reorder_quantity**: Standard reorder quantity
- **default_supplier**: Primary supplier for this product
- **is_active**: Whether product is available for sale
- **specs**: JSON field for additional specifications
- **created_by**: User who created this product record
- **created_at**: Date and time when record was created
- **updated_at**: Date and time when record was last updated

## Stock Model (core/models.py)

- **product**: Product this stock record belongs to (one-to-one)
- **quantity**: Current stock quantity
- **location**: Where the stock is stored (default: "Main Warehouse")
- **last_counted_at**: Date and time of last physical count
- **updated_at**: Date and time when record was last updated

## StockMovement Model (core/models.py)

- **product**: Product being moved
- **movement_type**: Type of movement: in, out, adjustment, transfer, return
- **quantity**: Quantity moved (positive or negative)
- **reference_type**: Type of document referencing this movement
- **reference_id**: ID of the referencing document
- **notes**: Additional notes about the movement
- **created_by**: User who recorded this movement
- **created_at**: Date and time when movement was recorded

## Invoice Model (core/models.py)

- **invoice_number**: Unique invoice number
- **customer**: Customer being invoiced
- **issue_date**: Date invoice was issued
- **due_date**: Date payment is due
- **subtotal**: Total before tax (12 digits, 2 decimals)
- **tax_amount**: Tax amount (12 digits, 2 decimals)
- **total_amount**: Total amount due (12 digits, 2 decimals)
- **paid_amount**: Amount already paid (12 digits, 2 decimals)
- **status**: Invoice status: draft, issued, partially_paid, paid, cancelled, overdue
- **is_approved**: Whether invoice has been approved
- **approved_by**: User who approved the invoice
- **approved_at**: Date and time of approval
- **notes**: Additional notes
- **created_by**: User who created the invoice
- **created_at**: Date and time when invoice was created
- **updated_at**: Date and time when invoice was last updated

## InvoiceItem Model (core/models.py)

- **invoice**: Invoice this item belongs to
- **product**: Product being sold
- **quantity**: Quantity sold
- **unit_price**: Price per unit (10 digits, 2 decimals)
- **tax_rate**: Tax rate as percentage (5 digits, 2 decimals)
- **total_price**: Total price for this item (12 digits, 2 decimals)

## Receipt Model (core/models.py)

- **receipt_number**: Unique receipt number
- **supplier**: Supplier sending the goods
- **receipt_date**: Date goods were received
- **subtotal**: Total before tax (12 digits, 2 decimals)
- **tax_amount**: Tax amount (12 digits, 2 decimals)
- **total_amount**: Total amount (12 digits, 2 decimals)
- **status**: Receipt status: draft, received, verified, cancelled
- **is_approved**: Whether receipt has been approved
- **approved_by**: User who approved the receipt
- **approved_at**: Date and time of approval
- **po_number**: Purchase order number
- **notes**: Additional notes
- **created_by**: User who created the receipt
- **created_at**: Date and time when receipt was created
- **updated_at**: Date and time when receipt was last updated

## ReceiptItem Model (core/models.py)

- **receipt**: Receipt this item belongs to
- **product**: Product received
- **quantity_ordered**: Quantity that was ordered
- **quantity_received**: Quantity actually received
- **unit_price**: Price per unit (10 digits, 2 decimals)
- **tax_rate**: Tax rate as percentage (5 digits, 2 decimals)
- **total_price**: Total price for this item (12 digits, 2 decimals)
- **notes**: Notes about this item

## Debt Model (core/models.py)

- **customer**: Customer who owes the money
- **invoice**: Invoice this debt relates to (optional)
- **original_amount**: Original amount owed (12 digits, 2 decimals)
- **paid_amount**: Amount already paid (12 digits, 2 decimals)
- **status**: Debt status: pending, partially_paid, paid, overdue, written_off
- **due_date**: Date payment is due
- **reminder_sent_at**: Date and time last reminder was sent
- **last_payment_date**: Date of last payment
- **days_overdue**: Number of days past due date
- **collection_attempts**: Number of collection attempts made
- **notes**: Additional notes about the debt
- **created_by**: User who created the debt record
- **created_at**: Date and time when debt was created
- **updated_at**: Date and time when debt was last updated

## DebtPayment Model (core/models.py)

- **debt**: Debt this payment applies to
- **amount**: Payment amount (12 digits, 2 decimals)
- **payment_date**: Date payment was made
- **payment_method**: Method of payment: cash, check, bank_transfer, credit_card, other
- **reference_number**: Reference number for the payment
- **notes**: Additional notes about the payment
- **recorded_by**: User who recorded the payment
- **created_at**: Date and time when payment was recorded

## AuditLog Model (core/models.py)

- **user**: User who performed the action
- **action**: Action performed: create, update, delete, approve, reject, view, export, login, logout
- **model_name**: Name of the model affected
- **object_id**: ID of the object affected
- **object_description**: Description of the object
- **old_values**: JSON of old field values
- **new_values**: JSON of new field values
- **ip_address**: IP address of the user
- **user_agent**: Browser/client user agent string
- **timestamp**: Date and time of the action

## ManagerDashboardMetrics Model (core/models.py)

- **total_invoices_issued**: Total number of invoices created
- **total_receipts_received**: Total number of receipts processed
- **total_outstanding_debt**: Total amount of outstanding debt
- **total_overdue_debt**: Total amount of overdue debt
- **pending_approvals**: Number of items waiting for approval
- **low_stock_products**: Number of products below reorder level
- **total_customers**: Total number of customers
- **total_suppliers**: Total number of suppliers
- **last_updated**: Date and time of last metric update</content>
<parameter name="filePath">x:\WEB\BUSINESS\inventory-mgt-system\MODELS_REFERENCE.md