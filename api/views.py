from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from core.models import Product, Category

@login_required
@require_GET
def device_list_api(request):
    """
    Returns a JSON list of products with optional filtering.
    
    Query Parameters:
    - category: Filter by category ID
    - is_active: Filter by active status
    
    Returns JSON with products list.
    """
    products = Product.objects.select_related('category', 'created_by').all()
    category = request.GET.get('category')
    is_active = request.GET.get('is_active')

    if category:
        products = products.filter(category__id=category)
    if is_active:
        products = products.filter(is_active=True)

    data = []
    for product in products:
        data.append({
            'id': product.id,
            'code': product.code,
            'name': product.name,
            'category': product.category.name,
            'cost_price': str(product.cost_price),
            'selling_price': str(product.selling_price),
            'quantity_in_stock': product.quantity_in_stock,
            'created_by': product.created_by.username if product.created_by else 'System',
        })

    return JsonResponse({'products': data})

@login_required
@require_GET
def device_search_api(request):
    """
    Returns search suggestions for products based on query string.
    
    Query Parameters:
    - q: Search query string (searches in product names and codes)
    
    Returns JSON with suggestions list.
    """
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)[:10]
    data = [{'id': p.id, 'code': p.code, 'name': p.name} for p in products]
    return JsonResponse({'suggestions': data})
