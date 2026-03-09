from django.contrib import admin
from .models import Category, Tag, Device, DeviceComparison

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for managing device categories.
    """
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin interface for managing device tags.
    """
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    """
    Admin interface for managing devices with filtering and search capabilities.
    """
    list_display = ('name', 'type', 'category', 'created_by', 'created_at')
    list_filter = ('type', 'category', 'created_at')
    search_fields = ('name', 'description')
    filter_horizontal = ('tags',)

@admin.register(DeviceComparison)
class DeviceComparisonAdmin(admin.ModelAdmin):
    """
    Admin interface for managing device comparisons.
    """
    list_display = ('device1', 'device2', 'created_by', 'created_at')
    search_fields = ('device1__name', 'device2__name')
