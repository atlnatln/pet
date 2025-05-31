"""
🐾 Kullanıcı Permissions
==============================================================================
Kullanıcı yetkilendirme sistemi - Güvenli erişim kontrolü
==============================================================================
"""

from rest_framework import permissions
from rest_framework.permissions import BasePermission
from django.utils.translation import gettext_lazy as _
from apps.ortak.constants import UserRoles, UserStatus


class IsProfileOwner(BasePermission):
    """
    Sadece profil sahibi erişebilir
    """
    
    def has_object_permission(self, request, view, obj):
        # Profil sahibi veya admin erişebilir
        return (
            request.user.is_authenticated and 
            (obj == request.user or request.user.rol == UserRoles.ADMIN)
        )


class IsVerifiedUser(BasePermission):
    """
    Sadece doğrulanmış kullanıcılar erişebilir
    """
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.email_dogrulanmis and
            request.user.durum == UserStatus.ACTIVE
        )


class CanAdoptPets(BasePermission):
    """
    Hayvan sahiplenme yetkisi
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Doğrulanmış ve sahiplenmek isteyen kullanıcılar
        return (
            request.user.email_dogrulanmis and
            request.user.durum == UserStatus.ACTIVE and
            request.user.sahiplenmek_istiyor_mu
        )


class CanListPets(BasePermission):
    """
    Hayvan listeleme yetkisi
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Doğrulanmış ve sahiplendiren kullanıcılar
        return (
            request.user.email_dogrulanmis and
            request.user.durum == UserStatus.ACTIVE and
            request.user.sahiplendiren_mi
        )


class IsModeratorOrAdmin(BasePermission):
    """
    Moderatör veya admin yetkisi
    """
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.rol in [UserRoles.MODERATOR, UserRoles.ADMIN]
        )


class IsVeterinaryOrAdmin(BasePermission):
    """
    Veteriner veya admin yetkisi
    """
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.rol in [UserRoles.VETERINARY, UserRoles.ADMIN]
        )


class CanModifyProfile(BasePermission):
    """
    Profil düzenleme yetkisi
    """
    
    def has_object_permission(self, request, view, obj):
        # Okuma için herkese açık
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Yazma için sadece profil sahibi
        return (
            request.user.is_authenticated and
            obj == request.user
        )


class HasCompleteProfile(BasePermission):
    """
    Tamamlanmış profil gereksinimi
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        return request.user.profil_tamamlanmis_mi


class CanContactUsers(BasePermission):
    """
    Kullanıcılarla iletişim kurma yetkisi
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Doğrulanmış ve profili tamamlanmış kullanıcılar
        return (
            request.user.email_dogrulanmis and
            request.user.durum == UserStatus.ACTIVE and
            request.user.profil_tamamlama_yuzdesi >= 70  # En az %70 tamamlanmış
        )


# Compound permissions
class AdoptionPermissions(BasePermission):
    """
    Sahiplenme işlemleri için birleşik yetki
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        return all([
            request.user.email_dogrulanmis,
            request.user.durum == UserStatus.ACTIVE,
            request.user.profil_tamamlanmis_mi,
            hasattr(request.user, 'profil_detay'),
            request.user.profil_detay.kimlik_dogrulandi_mi if hasattr(request.user, 'profil_detay') else False
        ])


# Permission helper functions
def user_can_adopt(user):
    """
    Kullanıcı sahiplenme yapabilir mi?
    """
    if not user.is_authenticated:
        return False
    
    return (
        user.email_dogrulanmis and
        user.durum == UserStatus.ACTIVE and
        user.sahiplenmek_istiyor_mu and
        user.profil_tamamlanmis_mi
    )


def user_can_list_pets(user):
    """
    Kullanıcı hayvan listesi oluşturabilir mi?
    """
    if not user.is_authenticated:
        return False
    
    return (
        user.email_dogrulanmis and
        user.durum == UserStatus.ACTIVE and
        user.sahiplendiren_mi and
        user.profil_tamamlama_yuzdesi >= 60
    )


def user_can_moderate(user):
    """
    Kullanıcı moderasyon yapabilir mi?
    """
    if not user.is_authenticated:
        return False
    
    return user.rol in [UserRoles.MODERATOR, UserRoles.ADMIN]

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Bu permission sistemi, platformun güvenliğini katmanlar halinde sağlar.
# Her işlem için uygun yetki kontrolü, kullanıcı deneyimini korur.
# 🐾 Güvenlik, sevginin en güzel koruyucusudur!
