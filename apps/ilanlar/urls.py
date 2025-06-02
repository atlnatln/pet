"""
📢 İlanlar URL Configuration
==============================================================================
İlan endpoint'lerinin route tanımları
==============================================================================
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IlanViewSet, IlanBasvuruViewSet

app_name = 'ilanlar'

# DRF Router
router = DefaultRouter()
router.register(r'ilanlar', IlanViewSet, basename='ilan')
router.register(r'basvurular', IlanBasvuruViewSet, basename='basvuru')

urlpatterns = [
    # API routes
    path('', include(router.urls)),
]

# ==============================================================================
# 🌐 AVAILABLE ENDPOINTS
# ==============================================================================
"""
📋 İlan API Endpoint'leri:

🔸 GET /api/v1/ilanlar/
   - Tüm ilanları listele (filtreleme + arama destekli)

🔸 GET /api/v1/ilanlar/{id}/
   - İlan detayı

🔸 POST /api/v1/ilanlar/
   - Yeni ilan oluştur (kimlik doğrulama gerekli)

🔸 PUT/PATCH /api/v1/ilanlar/{id}/
   - İlan güncelle (kimlik doğrulama gerekli)

🔸 GET /api/v1/ilanlar/acil_ilanlar/
   - Acil ilanlar

🔸 GET /api/v1/ilanlar/son_ilanlar/
   - Son eklenen ilanlar

🔸 POST /api/v1/ilanlar/{id}/basvuru_yap/
   - İlana başvuru yap

🔸 GET /api/v1/basvurular/
   - Kullanıcının başvuruları
"""
