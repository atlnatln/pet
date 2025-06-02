"""
🐾 Kullanıcılar Modelleri
==============================================================================
Platform kullanıcıları için temel model yapısı
==============================================================================
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Özelleştirilmiş kullanıcı modeli
    Django'nun standart User modelini genişletir
    """
    
    # Telefon bilgisi
    telefon = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Telefon")
    )
    
    # Konum bilgisi
    il = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("İl")
    )
    
    # Profil fotoğrafı
    profil_fotografi = models.ImageField(
        upload_to='kullanicilar/profil/%Y/%m/',
        blank=True,
        null=True,
        verbose_name=_("Profil Fotoğrafı")
    )
    
    # Kullanıcı türü
    kullanici_turu = models.CharField(
        max_length=20,
        choices=[
            ('bireysel', _('Bireysel Kullanıcı')),
            ('baranak', _('Barınak')),
            ('veteriner', _('Veteriner')),
            ('petshop', _('Pet Shop')),
        ],
        default='bireysel',
        verbose_name=_("Kullanıcı Türü")
    )
    
    # Doğrulama durumları
    telefon_dogrulandimi = models.BooleanField(
        default=False,
        verbose_name=_("Telefon Doğrulandı")
    )
    
    class Meta:
        verbose_name = _("👤 Kullanıcı")
        verbose_name_plural = _("👥 Kullanıcılar")
    
    def __str__(self):
        return self.username or self.email
    
    @property
    def tam_ad(self):
        """Kullanıcının tam adı"""
        return f"{self.first_name} {self.last_name}".strip() or self.username
