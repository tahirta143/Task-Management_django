from django.contrib.auth.models import AbstractUser
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"

class User(AbstractUser):
    ADMIN = 'admin'
    MANAGER = 'manager'
    STAFF = 'staff'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (MANAGER, 'Manager'),
        (STAFF, 'Staff'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=STAFF)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')

    def is_manager(self):
        return self.role == self.MANAGER
    
    def is_staff_member(self):
        return self.role == self.STAFF
        
    def is_admin(self):
        return self.role == self.ADMIN
