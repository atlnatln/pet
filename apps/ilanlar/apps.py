"""
🐾 İlanlar App Configuration
==============================================================================
Sahiplendirme ve barınak ilanlarının yönetimi
==============================================================================
"""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class IlanlarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.ilanlar'
    verbose_name = _('📢 Sahiplendirme İlanları')
    verbose_name_plural = _('📢 Sahiplendirme İlanları')
    
    def ready(self):
        """
        Uygulama hazır olduğunda çalışacak setup
        """
        # Sinyalleri import et
        import apps.ilanlar.signals
        
        print("📢 İlanlar sistemi hazır - Yuva arayan dostlar için!")
