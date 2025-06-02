"""
🐾 API v1 Ana URL Yapılandırması
==============================================================================
Platformun tüm API endpoint'lerinin merkezi yönlendirmesi
==============================================================================
"""

from django.urls import path, include

app_name = 'v1'

urlpatterns = [
    # Kategoriler API
    path('', include('apps.kategoriler.urls')),
    
    # Hayvanlar API  
    path('', include('apps.hayvanlar.urls')),
    
    # İlanlar API
    path('', include('apps.ilanlar.urls')),
]

# ==============================================================================
# 🌐 API ENDPOINT OZETI
# ==============================================================================
"""
📋 Platform API v1 Endpoint'leri:

🏷️ KATEGORİLER (/api/v1/kategoriler/):
   - GET /kategoriler/ - Tüm kategoriler
   - GET /kategoriler/{id}/ - Kategori detayı
   - GET /kategoriler/ana_kategoriler/ - Ana kategoriler
   - GET /kategoriler/kategori_agaci/ - Hiyerarşik ağaç
   - GET /kategoriler/populer/ - Popüler kategoriler
   - GET /kategoriler/istatistikler/ - İstatistikler

🐾 HAYVANLAR (/api/v1/hayvanlar/):
   - GET /hayvanlar/ - Hayvan listesi
   - GET /hayvanlar/{id}/ - Hayvan detayı
   - POST /hayvanlar/ - Yeni hayvan ekle
   - GET /hayvanlar/populer/ - Popüler hayvanlar
   - GET /hayvanlar/son_eklenenler/ - Son eklenenler
   
🐕 KÖPEK IRKLARI (/api/v1/kopek-irklari/):
   - GET /kopek-irklari/ - Irk listesi
   - GET /kopek-irklari/populer/ - Popüler ırklar
   - GET /kopek-irklari/yerli/ - Yerli ırklar

📢 İLANLAR (/api/v1/ilanlar/):
   - GET /ilanlar/ - İlan listesi
   - GET /ilanlar/{id}/ - İlan detayı
   - POST /ilanlar/ - Yeni ilan ekle
   - GET /ilanlar/acil_ilanlar/ - Acil ilanlar
   - GET /ilanlar/son_ilanlar/ - Son ilanlar
   - POST /ilanlar/{id}/basvuru_yap/ - İlana başvur

🎯 MVP Sistemi Tamamlandı! Kategoriler → Hayvanlar → İlanlar
"""
