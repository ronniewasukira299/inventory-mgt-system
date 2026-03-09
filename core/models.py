from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Device(models.Model):
    DEVICE_TYPES = [
        ('serial', 'Serial'),
        ('parallel', 'Parallel'),
    ]

    name = models.CharField(max_length=200, db_index=True)
    type = models.CharField(max_length=10, choices=DEVICE_TYPES, db_index=True)
    description = models.TextField()
    specs = models.JSONField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_index=True)
    tags = models.ManyToManyField(Tag, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # def clean(self):
    #     if self.device1 == self.device2:
    #         raise ValidationError("Cannot compare a device with itself.")

    def get_absolute_url(self):
        return reverse('core:device_detail', args=[self.pk])

class DeviceComparison(models.Model):
    device1 = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='comparisons_as_first')
    device2 = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='comparisons_as_second')
    comparison_data = models.JSONField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device1} vs {self.device2}"

    def clean(self):
        if self.device1 == self.device2:
            raise ValidationError("Cannot compare a device with itself.")

    class Meta:
        unique_together = ('device1', 'device2')
