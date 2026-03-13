from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from core.models import Product, Category, Invoice, Receipt, Debt, Customer, Supplier, StockMovement
from accounts.decorators import manager_required

# class based view for all the API endpoints replicating all the routes in core/views.py but with JSON responses instead of HTML templates
@login_required
@manager_required
@require_GET
def product_list_api(request):
    """API endpoint to list all products."""
    products = Product.objects.all().values('id', 'code', 'name', 'description', 'category__name', 'cost_price', 'selling_price', 'unit', 'quantity_in_stock', 'reorder_level', 'reorder_quantity', 'default_supplier__name', 'is_active')
    return JsonResponse(list(products), safe=False)

#Category API
@login_required
@manager_required
@require_GET
def category_list_api(request):
    """API endpoint to list all categories."""
    categories = Category.objects.all().values('id', 'name', 'description')
    return JsonResponse(list(categories), safe=False)

#Invoice API
@login_required
@manager_required
@require_GET
def invoice_list_api(request):
    """API endpoint to list all invoices."""
    invoices = Invoice.objects.all().values('id', 'invoice_number', 'customer__name', 'issue_date', 'due_date', 'notes')
    return JsonResponse(list(invoices), safe=False)

#Receipt API
@login_required
@manager_required
@require_GET
def receipt_list_api(request):
    """API endpoint to list all receipts."""
    receipts = Receipt.objects.all().values('id', 'receipt_number', 'supplier__name', 'receipt_date', 'notes')
    return JsonResponse(list(receipts), safe=False)

#Debt API
@login_required
@manager_required
@require_GET
def debt_list_api(request):
    """API endpoint to list all debts."""
    debts = Debt.objects.all().values('id', 'customer__name', 'amount', 'due_date', 'status')
    return JsonResponse(list(debts), safe=False)

#Customer API
@login_required
@manager_required
@require_GET
def customer_list_api(request):
    """API endpoint to list all customers."""
    customers = Customer.objects.all().values('id', 'name', 'email', 'phone', 'address')
    return JsonResponse(list(customers), safe=False)

#Supplier API
@login_required
@manager_required
@require_GET
def supplier_list_api(request):
    """API endpoint to list all suppliers."""
    suppliers = Supplier.objects.all().values('id', 'name', 'email', 'phone', 'address')
    return JsonResponse(list(suppliers), safe=False)

#Stock Movement API
@login_required
@manager_required
@require_GET
def stock_movement_list_api(request):
    """API endpoint to list all stock movements."""
    stock_movements = StockMovement.objects.all().values('id', 'product__name', 'quantity', 'movement_type', 'date', 'notes')
    return JsonResponse(list(stock_movements), safe=False)

