"""
🐾 Kullanıcılar Admin
==============================================================================
Kullanıcı yönetimi için admin arayüzü
==============================================================================
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Özelleştirilmiş kullanıcı admin arayüzü
    """
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'telefon', 'il', 'is_active']
    list_filter = ['is_active', 'is_staff', 'il']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'telefon']
    
    fieldsets = UserAdmin.fieldsets + (
        (_('Ek Bilgiler'), {
            'fields': ('telefon', 'il'),
        }),
    )
