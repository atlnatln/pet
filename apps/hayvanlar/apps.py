from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class HayvanlarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.hayvanlar'
    verbose_name = _('🐾 Hayvanlar')
    
    def ready(self):
        """
        Uygulama hazır olduğunda çalışacak setup
        """
        # Sinyalleri import et
        import apps.hayvanlar.signals
        
        print("🐾 Hayvanlar sistemi hazır - Can dostları dijital dünyada!")
