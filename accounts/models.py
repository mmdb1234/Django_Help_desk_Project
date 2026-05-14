from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'مشتری'),
        ('support', 'پشتیبان'),
        ('admin', 'مدیر'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True)
    avatar = models.URLField(blank=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"