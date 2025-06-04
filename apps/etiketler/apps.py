"""
🏷️ Evcil Hayvan Platformu - Etiketler Uygulaması Yapılandırma
==============================================================================
Etiketler uygulama yapılandırması
==============================================================================
"""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EtiketlerConfig(AppConfig):
    """Etiketler uygulaması yapılandırması"""
    name = 'apps.etiketler'
    verbose_name = _("🏷️ Etiketler")
    
    def ready(self):
        """Signals ve diğer modüllerin yüklenmesi"""
        from . import signals