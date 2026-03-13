from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Supplier, Customer, Category, Tag, Product, Stock, StockMovement,
    Invoice, InvoiceItem, Receipt, ReceiptItem,
    Debt, DebtPayment, AuditLog, ManagerDashboardMetrics
)
admin.site.site_title = "INVENTORY MANAGEMENT SYSTEM"
admin.site.site_header = "IMS ADMIN SITE"

# ============================================================================
# ORGANIZATION MANAGEMENT
# ============================================================================

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'status', 'rating', 'created_at')
    list_filter = ('status', 'created_at', 'rating')
    search_fields = ('name', 'email', 'contact_person', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'contact_person', 'email', 'phone')
        }),
        ('Address', {
            'fields': ('address', 'city', 'country', 'postal_code')
        }),
        ('Business Terms', {
            'fields': ('status', 'rating', 'credit_terms_days')
        }),
        ('Additional Info', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'status', 'credit_limit', 'credit_used', 'available_credit_display', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'contact_person', 'phone')
    readonly_fields = ('created_at', 'updated_at', 'available_credit_display')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'contact_person', 'email', 'phone')
        }),
        ('Address', {
            'fields': ('address', 'city', 'country', 'postal_code')
        }),
        ('Credit Management', {
            'fields': ('status', 'credit_limit', 'credit_used', 'available_credit_display', 'credit_terms_days')
        }),
        ('Additional Info', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def available_credit_display(self, obj):
        available = obj.available_credit
        color = 'green' if available > 0 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">${:.2f}</span>',
            color, available
        )
    available_credit_display.short_description = 'Available Credit'


# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'cost_price', 'selling_price', 'quantity_in_stock', 'is_low_stock_display', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at', 'unit')
    search_fields = ('code', 'name', 'description')
    filter_horizontal = ('tags',)
    readonly_fields = ('created_at', 'updated_at', 'is_low_stock_display', 'profit_margin_display')
    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'name', 'description', 'category', 'tags', 'is_active')
        }),
        ('Pricing', {
            'fields': ('cost_price', 'selling_price', 'profit_margin_display')
        }),
        ('Stock', {
            'fields': ('quantity_in_stock', 'reorder_level', 'reorder_quantity', 'unit', 'is_low_stock_display')
        }),
        ('Supplier', {
            'fields': ('default_supplier',)
        }),
        ('Specifications', {
            'fields': ('specs',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def is_low_stock_display(self, obj):
        color = 'red' if obj.is_low_stock else 'green'
        status = 'LOW' if obj.is_low_stock else 'OK'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, status
        )
    is_low_stock_display.short_description = 'Stock Status'

    def profit_margin_display(self, obj):
        return f"{obj.profit_margin:.2f}%"
    profit_margin_display.short_description = 'Profit Margin'


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'location', 'last_counted_at', 'updated_at')
    list_filter = ('location', 'updated_at')
    search_fields = ('product__code', 'product__name')
    readonly_fields = ('updated_at',)


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'movement_type', 'quantity', 'reference_type', 'created_by', 'created_at')
    list_filter = ('movement_type', 'created_at')
    search_fields = ('product__code', 'product__name', 'notes')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'


# ============================================================================
# INVOICING & RECEIPTS
# ============================================================================

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    fields = ('product', 'quantity', 'unit_price', 'tax_rate', 'total_price')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'customer', 'issue_date', 'due_date', 'total_amount', 'paid_amount', 'status', 'is_approved')
    list_filter = ('status', 'issue_date', 'is_approved')
    search_fields = ('invoice_number', 'customer__name')
    readonly_fields = ('created_at', 'updated_at', 'outstanding_amount', 'is_overdue')
    inlines = [InvoiceItemInline]
    fieldsets = (
        ('Invoice Information', {
            'fields': ('invoice_number', 'customer', 'issue_date', 'due_date')
        }),
        ('Amounts', {
            'fields': ('subtotal', 'tax_amount', 'total_amount', 'paid_amount', 'outstanding_amount', 'is_overdue')
        }),
        ('Status & Approval', {
            'fields': ('status', 'is_approved', 'approved_by', 'approved_at')
        }),
        ('Additional Info', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'issue_date'

    def outstanding_amount(self, obj):
        return f"${obj.outstanding_amount:.2f}"
    outstanding_amount.short_description = 'Outstanding Amount'

    def is_overdue(self, obj):
        color = 'red' if obj.is_overdue else 'green'
        status = 'OVERDUE' if obj.is_overdue else 'OK'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, status
        )
    is_overdue.short_description = 'Overdue Status'


class ReceiptItemInline(admin.TabularInline):
    model = ReceiptItem
    extra = 1
    fields = ('product', 'quantity_ordered', 'quantity_received', 'unit_price', 'tax_rate', 'total_price')


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'supplier', 'receipt_date', 'total_amount', 'status', 'is_approved')
    list_filter = ('status', 'receipt_date', 'is_approved')
    search_fields = ('receipt_number', 'supplier__name', 'po_number')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ReceiptItemInline]
    fieldsets = (
        ('Receipt Information', {
            'fields': ('receipt_number', 'supplier', 'receipt_date', 'po_number')
        }),
        ('Amounts', {
            'fields': ('subtotal', 'tax_amount', 'total_amount')
        }),
        ('Status & Approval', {
            'fields': ('status', 'is_approved', 'approved_by', 'approved_at')
        }),
        ('Additional Info', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'receipt_date'


# ============================================================================
# DEBT MANAGEMENT
# ============================================================================

class DebtPaymentInline(admin.TabularInline):
    model = DebtPayment
    extra = 1
    fields = ('amount', 'payment_date', 'payment_method', 'reference_number')
    readonly_fields = ('created_at',)


@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'original_amount', 'paid_amount', 'outstanding_amount_display', 'due_date', 'status', 'days_overdue')
    list_filter = ('status', 'due_date', 'created_at')
    search_fields = ('customer__name', 'notes')
    readonly_fields = ('created_at', 'updated_at', 'outstanding_amount_display', 'is_overdue')
    inlines = [DebtPaymentInline]
    fieldsets = (
        ('Debt Information', {
            'fields': ('customer', 'invoice', 'due_date')
        }),
        ('Amounts', {
            'fields': ('original_amount', 'paid_amount', 'outstanding_amount_display')
        }),
        ('Status & Tracking', {
            'fields': ('status', 'days_overdue', 'is_overdue', 'collection_attempts', 'last_payment_date', 'reminder_sent_at')
        }),
        ('Additional Info', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'due_date'

    def outstanding_amount_display(self, obj):
        color = 'red' if obj.outstanding_amount > 0 else 'green'
        return format_html(
            '<span style="color: {}; font-weight: bold;">${:.2f}</span>',
            color, obj.outstanding_amount
        )
    outstanding_amount_display.short_description = 'Outstanding Amount'

    def is_overdue(self, obj):
        color = 'red' if obj.is_overdue else 'green'
        status = 'OVERDUE' if obj.is_overdue else 'OK'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, status
        )
    is_overdue.short_description = 'Overdue Status'


@admin.register(DebtPayment)
class DebtPaymentAdmin(admin.ModelAdmin):
    list_display = ('debt', 'amount', 'payment_date', 'payment_method', 'recorded_by', 'created_at')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('debt__customer__name', 'reference_number')
    readonly_fields = ('created_at',)
    date_hierarchy = 'payment_date'


# ============================================================================
# AUDIT & MONITORING
# ============================================================================

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'model_name', 'object_description', 'timestamp')
    list_filter = ('action', 'model_name', 'timestamp')
    search_fields = ('user__username', 'model_name', 'object_description')
    readonly_fields = ('user', 'action', 'model_name', 'object_id', 'object_description', 
                       'old_values', 'new_values', 'ip_address', 'user_agent', 'timestamp')
    date_hierarchy = 'timestamp'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(ManagerDashboardMetrics)
class ManagerDashboardMetricsAdmin(admin.ModelAdmin):
    list_display = ('last_updated', 'total_invoices_issued', 'total_receipts_received', 
                   'total_outstanding_debt', 'total_overdue_debt', 'pending_approvals')
    readonly_fields = ('total_invoices_issued', 'total_receipts_received', 'total_outstanding_debt',
                      'total_overdue_debt', 'pending_approvals', 'low_stock_products', 
                      'total_customers', 'total_suppliers', 'last_updated')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
