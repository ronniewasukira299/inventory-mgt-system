from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # URL name: 'accounts:login' - Use in templates: {% url 'accounts:login' %}
    path('login/', views.login_view, name='login'),

    # URL name: 'accounts:logout' - Use in templates: {% url 'accounts:logout' %}
    path('logout/', views.logout_view, name='logout'),

    # URL name: 'accounts:register' - Use in templates: {% url 'accounts:register' %}
    path('register/', views.register_view, name='register'),

    # URL name: 'accounts:password_reset' - Use in templates: {% url 'accounts:password_reset' %}
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),

    # URL name: 'accounts:password_reset_done' - Use in templates: {% url 'accounts:password_reset_done' %}
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),

    # URL name: 'accounts:password_reset_confirm' - Use in templates: {% url 'accounts:password_reset_confirm' %}
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),

    # URL name: 'accounts:password_reset_complete' - Use in templates: {% url 'accounts:password_reset_complete' %}
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),

    # URL name: 'accounts:profile' - Use in templates: {% url 'accounts:profile' %}
    path('profile/', views.profile_view, name='profile'),
]