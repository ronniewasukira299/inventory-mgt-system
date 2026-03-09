from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('devices/', views.device_list_api, name='device_list_api'),
    path('search/', views.device_search_api, name='device_search_api'),
]