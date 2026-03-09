from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.DeviceListView.as_view(), name='device_list'),
    path('device/<int:pk>/', views.DeviceDetailView.as_view(), name='device_detail'),
    path('compare/<int:pk1>/<int:pk2>/', views.device_comparison_view, name='device_comparison'),
    path('contact/', views.contact_view, name='contact'),
]