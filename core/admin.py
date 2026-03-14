from django.contrib import admin
from django.utils.html import format_html
from .models import Supplier, Product, StockMovement

admin.site.site_title = "INVENTORY MANAGEMENT SYSTEM"
admin.site.site_header = "IMS ADMIN SITE"


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'phone', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'email', 'contact_person', 'phone')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier', 'unit_price', 'stock_quantity', 'is_low_stock_display', 'is_active')
    list_filter = ('is_active', 'supplier')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

    def is_low_stock_display(self, obj):
        color = 'red' if obj.is_low_stock else 'green'
        status = 'LOW' if obj.is_low_stock else 'OK'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, status
        )
    is_low_stock_display.short_description = 'Stock Status'


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'movement_type', 'quantity', 'created_by', 'created_at')
    list_filter = ('movement_type', 'created_at')
    search_fields = ('product__name', 'notes')
    readonly_fields = ('created_at',)