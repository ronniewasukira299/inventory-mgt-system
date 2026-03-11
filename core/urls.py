from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Product management (keeping old device URLs for compatibility)
    path('', views.DeviceListView.as_view(), name='device_list'),
    path('device/<int:pk>/', views.DeviceDetailView.as_view(), name='device_detail'),
    path('compare/<int:pk1>/<int:pk2>/', views.device_comparison_view, name='device_comparison'),
    
    # Manager Dashboard
    path('dashboard/', views.ManagerDashboardView.as_view(), name='manager_dashboard'),
    
    # Contact
    path('contact/', views.contact_view, name='contact'),
]