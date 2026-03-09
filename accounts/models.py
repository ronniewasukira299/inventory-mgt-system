from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('viewer', 'Viewer'),
    ]

    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='viewer')
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
