from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from core.models import Device, Category

@login_required
@require_GET
def device_list_api(request):
    """
    Returns a JSON list of devices with optional filtering.
    
    Query Parameters:
    - type: Filter by device type (serial, parallel)
    - category: Filter by category ID
    
    Returns JSON with devices list.
    """
    devices = Device.objects.select_related('category', 'created_by').all()
    device_type = request.GET.get('type')
    category = request.GET.get('category')

    if device_type:
        devices = devices.filter(type=device_type)
    if category:
        devices = devices.filter(category__id=category)

    data = []
    for device in devices:
        data.append({
            'id': device.id,
            'name': device.name,
            'type': device.type,
            'category': device.category.name,
            'specs': device.specs,
            'created_by': device.created_by.username,
        })

    return JsonResponse({'devices': data})

@login_required
@require_GET
def device_search_api(request):
    """
    Returns search suggestions for devices based on query string.
    
    Query Parameters:
    - q: Search query string (searches in device names)
    
    Returns JSON with suggestions list.
    """
    query = request.GET.get('q', '')
    devices = Device.objects.filter(name__icontains=query)[:10]
    data = [{'id': d.id, 'name': d.name} for d in devices]
    return JsonResponse({'suggestions': data})
