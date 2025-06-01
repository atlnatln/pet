"""
🐾 Evcil Hayvan Platformu - Hayvan URL'leri
==============================================================================
Hayvanlar için API endpoint'leri
==============================================================================
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HayvanViewSet, KopekIrkViewSet

app_name = 'hayvanlar'

# DRF Router
router = DefaultRouter()
router.register(r'hayvanlar', HayvanViewSet, basename='hayvan')
router.register(r'kopek-irklari', KopekIrkViewSet, basename='kopek-irklari')

urlpatterns = [
    # API routes
    path('', include(router.urls)),
]

# ==============================================================================
# 🌐 AVAILABLE ENDPOINTS
# ==============================================================================
"""
📋 Hayvan API Endpoint'leri:

🔸 GET /api/v1/hayvanlar/
   - Tüm hayvanları listele (filtreleme + arama destekli)

🔸 GET /api/v1/hayvanlar/{id}/
   - Hayvan detayı

🔸 POST /api/v1/hayvanlar/
   - Yeni hayvan oluştur (kimlik doğrulama gerekli)

🔸 PUT/PATCH /api/v1/hayvanlar/{id}/
   - Hayvan güncelle (kimlik doğrulama gerekli)

🔸 DELETE /api/v1/hayvanlar/{id}/
   - Hayvanı sil (kimlik doğrulama gerekli)

🔸 POST /api/v1/hayvanlar/{id}/fotograf_ekle/
   - Hayvana fotoğraf ekle (kimlik doğrulama gerekli)

🔸 GET /api/v1/hayvanlar/populer/
   - En popüler hayvanlar

🔸 GET /api/v1/hayvanlar/son_eklenenler/
   - Son eklenen hayvanlar

🔸 GET /api/v1/kopek-irklari/
   - Köpek ırklarını listele

🔸 GET /api/v1/kopek-irklari/{id}/
   - Köpek ırkı detayı

🔸 GET /api/v1/kopek-irklari/populer/
   - Popüler köpek ırkları

🔸 GET /api/v1/kopek-irklari/yerli/
   - Yerli köpek ırkları
"""
