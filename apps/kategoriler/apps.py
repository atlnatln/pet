"""
🐾 Kategoriler App Configuration
==============================================================================
Hayvan türlerinin organize edildiği dijital ansiklopedi
==============================================================================
"""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class KategorilerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.kategoriler'
    verbose_name = _('🏷️ Hayvan Kategorileri')
    verbose_name_plural = _('🏷️ Hayvan Kategorileri')
    
    def ready(self):
        """
        Uygulama hazır olduğunda çalışacak setup
        """
        # Future: signals import edilecek
        # import apps.kategoriler.signals  # noqa
        
        # Kategori sistem mesajı
        print("🏷️ Kategoriler sistemi hazır - Hayvan türleri organize edildi!")
