"""
🏷️ Etiketler App Configuration
==============================================================================
Hayvan özelliklerinin etiketlendiği dinamik sınıflandırma sistemi
==============================================================================
"""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EtiketlerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.etiketler'
    verbose_name = _('🏷️ Etiketler')
    verbose_name_plural = _('🏷️ Etiket Sistemi')
    
    def ready(self):
        """
        Uygulama hazır olduğunda çalışacak setup
        """
        # Sinyalleri import et
        try:
            import apps.etiketler.signals
        except ImportError:
            pass
        
        print("🏷️ Etiket sistemi hazır - Hayvan karakteristikleri etiketleniyor!")
