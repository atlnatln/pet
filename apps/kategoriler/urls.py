"""
🐾 Kategoriler URL Configuration
==============================================================================
Kategori endpoint'lerinin route tanımları
==============================================================================
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KategoriViewSet

app_name = 'kategoriler'

# DRF Router
router = DefaultRouter()
router.register(r'kategoriler', KategoriViewSet, basename='kategori')

urlpatterns = [
    # API v1 routes
    path('', include(router.urls)),
    
    # Custom URL patterns (if needed)
    # path('custom-endpoint/', CustomView.as_view(), name='custom'),
]

# ==============================================================================
# 🌐 AVAILABLE ENDPOINTS
# ==============================================================================
"""
📋 Kategori API Endpoint'leri:

🔸 GET /api/v1/kategoriler/
   - Tüm kategorileri listele (filtreleme + arama destekli)

🔸 GET /api/v1/kategoriler/{id}/
   - Kategori detayı (alt kategoriler ve özellikler dahil)

🔸 POST /api/v1/kategoriler/
   - Yeni kategori oluştur (admin yetkisi gerekli)

🔸 PUT/PATCH /api/v1/kategoriler/{id}/
   - Kategori güncelle (admin yetkisi gerekli)

🔸 DELETE /api/v1/kategoriler/{id}/
   - Kategori sil (admin yetkisi gerekli)

🔸 GET /api/v1/kategoriler/ana_kategoriler/
   - Sadece ana kategoriler

🔸 GET /api/v1/kategoriler/kategori_agaci/
   - Hiyerarşik kategori ağacı

🔸 GET /api/v1/kategoriler/{id}/alt_kategoriler/
   - Belirli kategorinin alt kategorileri

🔸 GET /api/v1/kategoriler/populer/
   - En popüler kategoriler

🔸 GET /api/v1/kategoriler/istatistikler/
   - Kategori istatistikleri

🔸 POST /api/v1/kategoriler/filtrele/
   - Gelişmiş filtreleme

🎯 Her endpoint, kategorilerin hikayesini farklı açılardan anlatır!
"""
