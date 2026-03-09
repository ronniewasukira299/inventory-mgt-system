from .models import Category

def site_nav(request):
    return {
        'categories': Category.objects.all(),
        'user_role': request.user.role if request.user.is_authenticated else None,
    }