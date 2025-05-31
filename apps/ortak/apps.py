"""
🐾 Evcil Hayvan Platformu - Ortak App Configuration
==============================================================================
Ortak modüller uygulaması konfigürasyonu
==============================================================================
"""

from django.apps import AppConfig


class OrtakConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.ortak'
    verbose_name = 'Ortak Modüller'
