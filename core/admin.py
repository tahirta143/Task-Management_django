from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'email')

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'company', 'is_staff')
    list_filter = ('role', 'company', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Company Info', {'fields': ('role', 'company')}),
    )

