"""
🐾 Evcil Hayvan Platformu - Main URL Configuration
==============================================================================
Bu dosya, platformun ana URL yönlendirme merkezi.
Her endpoint, hayvan sevgisini doğru hedefe ulaştırır.

API versioning, güvenlik ve performans odaklı tasarlanmıştır.
==============================================================================
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
import json
from datetime import datetime

# ==============================================================================
# 💝 PLATFORM HEALTH CHECK - Sevgi nabzı kontrolü
# ==============================================================================

@require_http_methods(["GET"])
@cache_page(60)  # 1 dakika cache
def health_check(request):
    """
    Platform sağlık durumu kontrolü
    Monitoring ve load balancer'lar için kritik endpoint
    """
    return JsonResponse({
        'status': 'healthy',
        'message': 'Evcil Hayvan Platformu çalışıyor! 🐾',
        'version': getattr(settings, 'VERSION', '1.0.0'),
        'environment': getattr(settings, 'ENVIRONMENT', 'unknown'),
        'timestamp': datetime.now().isoformat(),
        'django_version': getattr(settings, 'DJANGO_VERSION', '4.2'),
    })

@require_http_methods(["GET"])
def platform_info(request):
    """
    Platform genel bilgileri
    Frontend için platform meta verisi
    """
    return JsonResponse({
        'platform': {
            'name': 'Evcil Hayvan Platformu',
            'description': 'Sevgi köprüleri kuran dijital yuva',
            'version': getattr(settings, 'VERSION', '1.0.0'),
            'supported_languages': ['tr', 'en'],
            'features': {
                'pet_adoption': True,
                'messaging': True,
                'favorites': True,
                'notifications': True,
                'blog': True,
            }
        },
        'contact': {
            'support_email': 'destek@evcilhayvanplatformu.com',
            'emergency_email': 'acil@evcilhayvanplatformu.com',
        }
    })

# ==============================================================================
# 🎯 CORE URL PATTERNS - Ana yönlendirme sistemi
# ==============================================================================

urlpatterns = [
    # ==============================================================================
    # 🛡️ ADMIN INTERFACE - Güvenli yönetim merkezi
    # ==============================================================================
    path('admin/sevgi-yonetimi/', admin.site.urls),  # Güvenlik için özel isim
    
    # ==============================================================================
    # 💊 HEALTH & MONITORING - Sistem sağlık kontrolleri
    # ==============================================================================
    path('health/', health_check, name='health-check'),
    path('health/detailed/', include('health_check.urls')),  # Django health check app
    path('api/platform-info/', platform_info, name='platform-info'),
    
    # ==============================================================================
    # 🌊 API ENDPOINTS - RESTful servisler
    # ==============================================================================
    
    # API v1 - Mevcut stable API
    path('api/v1/', include('apps.api.v1.urls'), name='api-v1'),
    
    # Core platform endpoints (apps oluştukça eklenecek)
    # path('api/auth/', include('apps.kullanicilar.urls'), name='auth'),
    # path('api/hayvanlar/', include('apps.hayvanlar.urls'), name='hayvanlar-api'),
    # path('api/ilanlar/', include('apps.ilanlar.urls'), name='ilanlar-api'),
    
    # ==============================================================================
    # 📚 API DOCUMENTATION - Geliştirici dostu dokümantasyon
    # ==============================================================================
    path('api/docs/', TemplateView.as_view(
        template_name='docs/api_docs.html',
        extra_context={'title': 'Evcil Hayvan Platformu API Dokümantasyonu'}
    ), name='api-docs'),
    
    # ==============================================================================
    # 🎨 FRONTEND INTEGRATION - React App entegrasyonu
    # ==============================================================================
    
    # React Router için catch-all pattern
    # Tüm frontend route'ları React'a yönlendirilir
    re_path(r'^(?!(api|admin|health|media|static)/).*$', 
            TemplateView.as_view(template_name='index.html'), 
            name='frontend'),
]

# ==============================================================================
# 🔧 DEVELOPMENT STATIC/MEDIA SERVING - Geliştirme ortamı dosya servisi
# ==============================================================================

if settings.DEBUG:
    # Development'ta static ve media dosyalarını Django ile serve et
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Debug toolbar (eğer yüklüyse)
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

# ==============================================================================
# 🚨 CUSTOM ERROR HANDLERS - Özel hata yönetimi
# ==============================================================================

def custom_404_view(request, exception=None):
    """
    Özel 404 sayfa bulunamadı hatası
    Frontend için JSON response
    """
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Endpoint bulunamadı',
            'message': 'Aradığınız API endpoint mevcut değil. Lütfen dokümantasyonu kontrol edin.',
            'code': 404,
            'suggestion': 'API dokümantasyonu için /api/docs/ adresini ziyaret edin.'
        }, status=404)
    
    # Frontend için normal template döndür
    return TemplateView.as_view(template_name='errors/404.html')(request)

def custom_500_view(request):
    """
    Özel 500 sunucu hatası
    Güvenli error message ile user-friendly response
    """
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Sunucu hatası',
            'message': 'Üzgünüz, beklenmeyen bir hata oluştu. Ekibimiz bilgilendirildi.',
            'code': 500,
            'contact': 'Sorun devam ederse destek@evcilhayvanplatformu.com ile iletişime geçin.'
        }, status=500)
    
    return TemplateView.as_view(template_name='errors/500.html')(request)

def custom_403_view(request, exception=None):
    """
    Özel 403 yetkisiz erişim hatası
    """
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Yetkisiz erişim',
            'message': 'Bu kaynağa erişim yetkiniz bulunmuyor.',
            'code': 403,
            'suggestion': 'Giriş yapmanız veya yetki seviyenizi kontrol etmeniz gerekebilir.'
        }, status=403)
    
    return TemplateView.as_view(template_name='errors/403.html')(request)

# Error handler registration
handler404 = custom_404_view
handler500 = custom_500_view
handler403 = custom_403_view

# ==============================================================================
# 🎯 ADMIN INTERFACE CUSTOMIZATION - Admin panel özelleştirme
# ==============================================================================

# Admin site headers ve title'ları özelleştir
admin.site.site_header = "🐾 Evcil Hayvan Platformu Yönetimi"
admin.site.site_title = "Pet Platform Admin"
admin.site.index_title = "Sevgi Yönetim Merkezi"

# ==============================================================================
# 💝 PLATFORM BAŞLANGIC MESAJI
# ==============================================================================

if settings.DEBUG:
    print("""
    🐾 ===============================================
       Evcil Hayvan Platformu URL Configuration
    ===============================================
    
    📱 Admin: /admin/sevgi-yonetimi/
    🌊 API: /api/v1/
    📚 Docs: /api/docs/
    💊 Health: /health/
    
    💝 Her URL, bir hayvan hayatı için yapılandırıldı!
    ===============================================
    """)
