from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django_ratelimit.decorators import ratelimit
from .forms import UserRegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django_ratelimit.decorators import ratelimit
# from ratelimit import rate_limited as ratelimit
from .forms import UserRegisterForm

# @ratelimit(key='ip', rate='5/m', method='POST')
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('core:device_list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

# @ratelimit(key='ip', rate='3/m', method='POST')
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('core:device_list')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


# @ratelimit(key='ip', rate='5/m', method='POST')
def login_view(request):
    """
    Authenticates a user and logs them in. Rate limited to 5 attempts per minute.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('core:device_list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """
    Logs out the current user and redirects to login page.
    """
    logout(request)
    return redirect('accounts:login')

# @ratelimit(key='ip', rate='3/m', method='POST')
def register_view(request):
    """
    Registers a new user. Rate limited to 3 attempts per minute.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('core:device_list')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    """
    Displays the current user's profile information.
    """
    return render(request, 'accounts/profile.html', {'user': request.user})
