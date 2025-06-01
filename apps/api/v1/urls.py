"""
🐾 Pet API V1 URL Configuration
==============================================================================
API v1 endpoint'lerini düzenleyen merkez
==============================================================================
"""

from django.urls import path, include
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

# Ana router
router = DefaultRouter()

# Swagger şema view (drf_yasg yoksa yorum olarak kalacak)
try:
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    
    schema_view = get_schema_view(
        openapi.Info(
            title=_("🐾 Evcil Hayvan Platformu API"),
            default_version='v1',
            description=_("Evcil Hayvanlar için sevgi dolu API"),
            terms_of_service="https://www.petplatform.com/terms/",
            contact=openapi.Contact(email="contact@petplatform.com"),
            license=openapi.License(name="Özel Lisans"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )
    
    has_swagger = True
except ImportError:
    has_swagger = False

urlpatterns = [
    # API kök endpoint'i
    path('', include(router.urls)),
    
    # Token kimlik doğrulama
    path('token/', obtain_auth_token, name='token_obtain'),
    
    # App-specific URL'ler
    path('kullanicilar/', include('apps.kullanicilar.urls', namespace='kullanicilar')),
    
    # Kategoriler app'i URL'leri
    path('kategoriler/', include('apps.kategoriler.urls', namespace='kategoriler')),
]

# Swagger/OpenAPI dokümantasyonu (eğer drf_yasg yüklüyse)
if has_swagger:
    urlpatterns += [
        path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]

# Debug toolbar sadece geliştirme ortamında ve yüklüyse
if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),
        ]
    except ImportError:
        pass

# ==============================================================================
# 🌐 ENDPOINT INFO - API DOKÜMANTASYONU
# ==============================================================================
"""
📚 API V1 DOKÜMANTASYONU:

📁 Ana Endpointler:
    - /api/v1/                   → API kök - mevcut kaynaklar
    - /api/v1/docs/              → Interactive Swagger API dokümanı (requires drf-yasg)
    - /api/v1/redoc/             → ReDoc API dokümanı (requires drf-yasg)
    - /api/v1/token/             → Token based auth

📁 Kullanıcılar API:
    - /api/v1/kullanicilar/users/             → Kullanıcı listesi
    - /api/v1/kullanicilar/users/{id}/        → Kullanıcı detayı
    - /api/v1/kullanicilar/users/register/    → Kullanıcı kaydı
    - /api/v1/kullanicilar/users/me/          → Giriş yapmış kullanıcı
    - /api/v1/kullanicilar/users/login/       → Giriş
    - /api/v1/kullanicilar/users/logout/      → Çıkış

📁 Kategoriler API:
    - /api/v1/kategoriler/kategoriler/           → Kategori listesi
    - /api/v1/kategoriler/kategoriler/{id}/      → Kategori detayı
    - /api/v1/kategoriler/kategoriler/ana_kategoriler/ → Ana kategoriler
    - /api/v1/kategoriler/kategoriler/kategori_agaci/  → Kategori ağacı
    - /api/v1/kategoriler/kategoriler/populer/         → Popüler kategoriler
"""
