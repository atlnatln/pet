"""
🐾 Kullanıcılar App Configuration
==============================================================================
Kullanıcı yönetimi sistemi - Şimdilik temel yapı
==============================================================================
"""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class KullanicilarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.kullanicilar'
    verbose_name = _('👥 Kullanıcılar')
    verbose_name_plural = _('👥 Kullanıcılar')
    
    def ready(self):
        """
        Uygulama hazır olduğunda çalışacak setup
        """
        print("👥 Kullanıcılar sistemi hazır - Topluluk büyüyor!")
