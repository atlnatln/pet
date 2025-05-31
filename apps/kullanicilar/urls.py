"""
🐾 Kullanıcılar URL Configuration
==============================================================================
Kullanıcı endpoint'lerinin route tanımları
==============================================================================
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

app_name = 'kullanicilar'

# DRF Router
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

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
📋 Kullanıcı API Endpoint'leri:

🔐 Authentication Endpoints:
   POST /api/v1/users/register/
   - Yeni kullanıcı kaydı

   POST /api/v1/users/login/
   - Kullanıcı girişi

   POST /api/v1/users/logout/
   - Kullanıcı çıkışı

   POST /api/v1/users/verify_email/
   - E-posta doğrulama

   POST /api/v1/users/request_password_reset/
   - Şifre sıfırlama talebi

👤 Profil Endpoints:
   GET /api/v1/users/me/
   - Mevcut kullanıcı profili

   PUT/PATCH /api/v1/users/update_profile/
   - Profil güncelleme

   POST /api/v1/users/change_password/
   - Şifre değiştirme

   GET /api/v1/users/{id}/profil_detay/
   - Kullanıcı profil detayları

📊 Liste & Arama Endpoints:
   GET /api/v1/users/
   - Tüm kullanıcılar

   GET /api/v1/users/{id}/
   - Kullanıcı detayı

   GET /api/v1/users/sahiplendirenler/
   - Sahiplendiren kullanıcılar

   GET /api/v1/users/sahiplenmek_isteyenler/
   - Sahiplenmek isteyen kullanıcılar

   POST /api/v1/users/arama/
   - Kullanıcı arama

📈 İstatistik Endpoints:
   GET /api/v1/users/istatistikler/
   - Platform kullanıcı istatistikleri

🛡️ Moderasyon Endpoints:
   POST /api/v1/users/{id}/verify_identity/
   - Kimlik doğrulama (Moderatör/Admin)

🎯 Her endpoint, kullanıcı deneyimini önceleyerek tasarlandı!
"""
