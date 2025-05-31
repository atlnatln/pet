"""
🐾 Kullanıcılar App Configuration
==============================================================================
Platform kahramanlarının dijital kimlik yönetimi
==============================================================================
"""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class KullanicilarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.kullanicilar'
    verbose_name = _('👤 Platform Kullanıcıları')
    verbose_name_plural = _('👤 Platform Kullanıcıları')
    
    def ready(self):
        """
        Uygulama hazır olduğunda çalışacak setup
        """
        # Signals import edilecek
        # import apps.kullanicilar.signals  # noqa
        
        # Kullanıcı sistem mesajı
        print("👤 Kullanıcı sistemi hazır - Dijital kimlikler aktif!")
