from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


# ============================================================================
# CORE INVENTORY MODELS
# ============================================================================

class Supplier(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]

    name = models.CharField(max_length=200, unique=True, db_index=True)
    contact_person = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='suppliers_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='products')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='products_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('core:product_detail', args=[self.pk])

    @property
    def is_low_stock(self):
        return self.stock_quantity <= 10


class StockMovement(models.Model):
    MOVEMENT_TYPE_CHOICES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('adjustment', 'Adjustment'),
    ]

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='stock_movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES, db_index=True)
    quantity = models.IntegerField()
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='stock_movements_created')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.name} - {self.quantity}"