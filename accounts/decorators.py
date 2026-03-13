from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from functools import wraps

def manager_required(view_func):
    """
    Decorator that requires the user to be logged in and have manager role.
    Returns 403 Forbidden for staff users.
    """
    @login_required
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role != 'manager':
            return HttpResponseForbidden("Access denied. Manager role required.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view