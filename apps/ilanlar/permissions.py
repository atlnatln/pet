"""
📢 İlanlar Permissions
==============================================================================
İlan işlemleri için özel izin sınıfları
==============================================================================
"""

from rest_framework import permissions


class IsIlanOwnerOrReadOnly(permissions.BasePermission):
    """
    İlan sahibi veya sadece okuma izni
    """
    
    def has_object_permission(self, request, view, obj):
        # Okuma izinleri herkese açık
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Yazma izinleri sadece ilan sahibine
        # TODO: User modeli ile entegrasyon
        return True  # Şimdilik herkese izin ver


class CanCreateIlan(permissions.BasePermission):
    """
    İlan oluşturma izni
    """
    
    def has_permission(self, request, view):
        # Kullanıcı giriş yapmış olmalı
        if not request.user.is_authenticated:
            return False
        
        # TODO: Ek izin kontrolleri
        # - Kullanıcı doğrulanmış mı?
        # - Günlük ilan limiti var mı?
        # - Hesap durumu aktif mi?
        
        return True


class CanManageBasvuru(permissions.BasePermission):
    """
    Başvuru yönetme izni
    """
    
    def has_object_permission(self, request, view, obj):
        # Okuma izinleri
        if request.method in permissions.SAFE_METHODS:
            # Başvuru sahibi veya ilan sahibi görebilir
            # TODO: User entegrasyonu
            return True
        
        # Güncelleme izinleri sadece ilan sahibine
        # TODO: User entegrasyonu
        return True
