"""
🐾 Kullanıcı Managers
==============================================================================
Kullanıcı sorgulama ve yönetimi için özel manager'lar
==============================================================================
"""

from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models import Q, Count, Avg
from django.utils import timezone
from django.core.cache import cache
from apps.ortak.constants import UserStatus, UserRoles


class CustomUserManager(BaseUserManager):
    """
    Custom User Manager - Email tabanlı kullanıcı yönetimi
    """
    
    def create_user(self, email, password=None, **extra_fields):
        """
        Normal kullanıcı oluştur
        """
        if not email:
            raise ValueError('E-posta adresi zorunludur')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Süper kullanıcı oluştur
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', UserRoles.ADMIN)
        extra_fields.setdefault('email_dogrulanmis', True)
        extra_fields.setdefault('durum', UserStatus.ACTIVE)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser is_staff=True olmalı.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser is_superuser=True olmalı.')
        
        return self.create_user(email, password, **extra_fields)
    
    def aktif_kullanicilar(self):
        """
        🟢 Aktif kullanıcıları getir
        Sadece aktif (is_active=True) olan kullanıcıları döndürür
        """
        return self.filter(is_active=True)
    
    def email_dogrulanmamis(self):
        """E-posta doğrulanmamış kullanıcılar"""
        return self.filter(email_dogrulanmis=False)
    
    def sahiplendirenler(self):
        """
        🏠 Sahiplendiren kullanıcıları getir
        Sadece sahiplendiren rolündeki aktif kullanıcıları döndürür
        """
        return self.aktif_kullanicilar().filter(sahiplendiren_mi=True)
    
    def sahiplenmek_isteyenler(self):
        """
        💝 Sahiplenmek isteyen kullanıcıları getir
        Sadece sahiplenmek isteyen rolündeki aktif kullanıcıları döndürür
        """
        return self.aktif_kullanicilar().filter(sahiplenmek_istiyor_mu=True)
    
    def sehire_gore(self, sehir):
        """
        📍 Şehire göre kullanıcıları getir
        """
        return self.aktif_kullanicilar().filter(sehir__icontains=sehir)
    
    def deneyimli_kullanicilar(self):
        """Deneyimli kullanıcılar (profil detayı olan)"""
        return self.aktif_kullanicilar().filter(
            profil_detay__hayvan_deneyimi_yil__gte=1
        ).select_related('profil_detay')
    
    def email_ile_getir(self, email):
        """E-posta ile kullanıcı getir"""
        try:
            return self.get(email__iexact=email)
        except self.model.DoesNotExist:
            return None
    
    def arama_yap(self, query):
        """Kullanıcı arama"""
        if not query or len(query) < 2:
            return self.none()
        
        return self.aktif_kullanicilar().filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(biyografi__icontains=query)
        ).distinct()


class KullaniciProfilManager(models.Manager):
    """
    Kullanıcı profil detayları manager'ı
    """
    
    def tamamlanmis_profiller(self):
        """Tamamlanmış profiller"""
        return self.filter(
            kullanici__durum=UserStatus.ACTIVE,
            kullanici__email_dogrulanmis=True
        ).exclude(
            Q(hayvan_deneyimi_yil__isnull=True) |
            Q(ev_tipi='') |
            Q(referans_kisi_1='')
        )
    
    def kimlik_dogrulanmis(self):
        """Kimlik doğrulanmış profiller"""
        return self.filter(kimlik_dogrulandi_mi=True)
    
    def bahceli_evler(self):
        """Bahçeli evde yaşayanlar"""
        return self.filter(bahce_var_mi=True)
    
    def deneyimli_sahiplendirenler(self):
        """Deneyimli sahiplendirenler"""
        return self.filter(
            hayvan_deneyimi_yil__gte=2,
            daha_once_sahiplendin_mi=True
        ).select_related('kullanici')

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Bu manager'lar, kullanıcı sisteminin güçlü sorgu altyapısını sağlar.
# Email tabanlı authentication ve gelişmiş filtreleme özellikleri.
# 🐾 Her sorgu, doğru kullanıcıyı doğru zamanda bulur!
