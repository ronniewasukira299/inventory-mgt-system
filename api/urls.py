from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Product API endpoints
    path('products/', views.product_list_api, name='product_list_api'),

    # Category API endpoints
    path('categories/', views.category_list_api, name='category_list_api'),

    # Invoice API endpoints
    path('invoices/', views.invoice_list_api, name='invoice_list_api'),

    # Receipt API endpoints
    path('receipts/', views.receipt_list_api, name='receipt_list_api'),

    # Debt API endpoints
    path('debts/', views.debt_list_api, name='debt_list_api'),

    # Customer API endpoints
    path('customers/', views.customer_list_api, name='customer_list_api'),

    # Supplier API endpoints
    path('suppliers/', views.supplier_list_api, name='supplier_list_api'),

    # Stock Movement API endpoints
    path('stock-movements/', views.stock_movement_list_api, name='stock_movement_list_api'),
]