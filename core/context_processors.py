from .models import Product, Supplier, StockMovement

def site_nav(request):
    return {
        'low_stock_products': Product.objects.filter(is_active=True, stock_quantity__lte=10).count(),
        'user_role': request.user.role if request.user.is_authenticated else None,
    }