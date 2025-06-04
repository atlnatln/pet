"""
🏷️ Evcil Hayvan Platformu - Etiketler URLs
==============================================================================
Etiketler uygulaması için URL yapılandırmaları
==============================================================================
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import EtiketViewSet

# API router yapılandırması
router = DefaultRouter()
router.register(r'', EtiketViewSet, basename='etiket')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
]

# Uygulama adı
app_name = 'etiketler'