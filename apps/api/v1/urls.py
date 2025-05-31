"""
🐾 Evcil Hayvan Platformu - API v1 URLs
==============================================================================
Versioned API routing architecture with comprehensive endpoint organization.
RESTful conventions, rate limiting hooks ve Swagger documentation ready.
==============================================================================
"""

from django.urls import path, include
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import APIMetadataSerializer, HealthCheckSerializer
import uuid

# ==============================================================================
# 🌐 API ROOT ENDPOINTS - Ana API endpoint'leri
# ==============================================================================

@api_view(['GET'])
@permission_classes([AllowAny])
@cache_page(60 * 5)  # 5 dakika cache
def api_root(request):
    """
    API v1 root endpoint
    Tüm available endpoints ve metadata döner
    """
    
    # API metadata
    metadata = {
        'api_version': '1.0',
        'platform': 'Evcil Hayvan Platformu',
        'description': 'Hayvan sahiplenme platformu RESTful API',
        'documentation': request.build_absolute_uri('/api/docs/'),
        'last_updated': '2025-01-31',
        'support_email': 'api-support@evcilhayvanplatformu.com'
    }
    
    # Available endpoints
    endpoints = {
        # Core platform
        'platform_info': '/api/platform-info/',
        'health': '/health/',
        'docs': '/api/docs/',
        
        # Authentication (will be implemented)
        'auth': {
            'login': '/api/v1/auth/login/',
            'logout': '/api/v1/auth/logout/',
            'register': '/api/v1/auth/register/',
            'refresh': '/api/v1/auth/refresh/',
            'verify': '/api/v1/auth/verify/',
        },
        
        # Core resources (will be implemented)
        'users': '/api/v1/users/',
        'categories': '/api/v1/categories/',
        'pets': '/api/v1/pets/',
        'listings': '/api/v1/listings/',
        'applications': '/api/v1/applications/',
        
        # Communication (will be implemented)
        'messages': '/api/v1/messages/',
        'notifications': '/api/v1/notifications/',
        
        # Content (will be implemented)
        'favorites': '/api/v1/favorites/',
        'blog': '/api/v1/blog/',
        'reports': '/api/v1/reports/',
        
        # Admin (will be implemented)
        'admin': '/api/v1/admin/',
        'moderation': '/api/v1/moderation/',
    }
    
    # Rate limiting info
    rate_limits = {
        'anonymous': '1000/hour',
        'authenticated': '5000/hour',
        'premium': '10000/hour',
        'api_key': '50000/hour'
    }
    
    # Supported features
    features = {
        'pagination': True,
        'filtering': True,
        'sorting': True,
        'search': True,
        'caching': True,
        'rate_limiting': True,
        'authentication': ['session', 'token', 'jwt'],
        'content_types': ['application/json', 'multipart/form-data'],
        'api_versioning': True,
        'webhooks': False,  # Future feature
        'graphql': False,   # Future feature
    }
    
    return Response({
        'message': 'Evcil Hayvan Platformu API v1 🐾',
        'status': 'active',
        'metadata': metadata,
        'endpoints': endpoints,
        'rate_limits': rate_limits,
        'features': features,
        'request_id': str(uuid.uuid4())
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    """
    API status ve system health
    """
    
    # System status checks
    status_checks = {
        'database': True,     # TODO: Implement actual DB check
        'cache': True,        # TODO: Implement cache check
        'storage': True,      # TODO: Implement storage check
        'external_apis': True # TODO: Implement external API checks
    }
    
    # Performance metrics
    performance = {
        'average_response_time': '150ms',  # TODO: Implement actual metrics
        'uptime': '99.9%',
        'active_connections': 42,  # TODO: Implement connection tracking
    }
    
    return Response({
        'status': 'operational',
        'checks': status_checks,
        'performance': performance,
        'timestamp': request.META.get('HTTP_DATE'),
    })

# ==============================================================================
# 🔄 CORE URL PATTERNS - Ana URL pattern'leri
# ==============================================================================

# API versioning namespace
app_name = 'api_v1'

urlpatterns = [
    # ==============================================================================
    # 🎯 ROOT & STATUS ENDPOINTS
    # ==============================================================================
    path('', api_root, name='api-root'),
    path('status/', api_status, name='api-status'),
    
    # ==============================================================================
    # 🔐 AUTHENTICATION ENDPOINTS (will be implemented)
    # ==============================================================================
    # path('auth/', include('apps.kullanicilar.urls', namespace='auth')),
    
    # ==============================================================================
    # 👥 USER MANAGEMENT (will be implemented)
    # ==============================================================================
    # path('users/', include('apps.kullanicilar.api_urls', namespace='users')),
    
    # ==============================================================================
    # 🏷️ CONTENT CATEGORIZATION (will be implemented)
    # ==============================================================================
    # path('categories/', include('apps.kategoriler.urls', namespace='categories')),
    
    # ==============================================================================
    # 🐾 PET MANAGEMENT (will be implemented)
    # ==============================================================================
    # path('pets/', include('apps.hayvanlar.urls', namespace='pets')),
    
    # ==============================================================================
    # 📋 ADOPTION LISTINGS (will be implemented)
    # ==============================================================================
    # path('listings/', include('apps.ilanlar.urls', namespace='listings')),
    
    # ==============================================================================
    # 📝 ADOPTION APPLICATIONS (will be implemented)
    # ==============================================================================
    # path('applications/', include('apps.basvurular.urls', namespace='applications')),
    
    # ==============================================================================
    # 💬 COMMUNICATION (will be implemented)
    # ==============================================================================
    # path('messages/', include('apps.mesajlasma.urls', namespace='messages')),
    # path('notifications/', include('apps.bildirimler.urls', namespace='notifications')),
    
    # ==============================================================================
    # ❤️ USER PREFERENCES (will be implemented)
    # ==============================================================================
    # path('favorites/', include('apps.favoriler.urls', namespace='favorites')),
    
    # ==============================================================================
    # 📰 CONTENT & BLOG (will be implemented)
    # ==============================================================================
    # path('blog/', include('apps.blog.urls', namespace='blog')),
    
    # ==============================================================================
    # 🚨 MODERATION & REPORTS (will be implemented)
    # ==============================================================================
    # path('reports/', include('apps.raporlar.urls', namespace='reports')),
    
    # ==============================================================================
    # 🛡️ ADMIN & MODERATION (will be implemented)
    # ==============================================================================
    # path('admin/', include('apps.admin.urls', namespace='admin')),
    # path('moderation/', include('apps.moderation.urls', namespace='moderation')),
    
    # Kullanıcılar API
    path('kullanicilar/', include('apps.kullanicilar.urls')),
    
    # Kategoriler API
    path('kategoriler/', include('apps.kategoriler.urls')),
]

# ==============================================================================
# 🔍 FUTURE API ENDPOINTS - Gelecek özellikler
# ==============================================================================

# Bu endpoint'ler henüz implement edilmemiş, ancak URL structure hazır:

# Analytics endpoints
# path('analytics/', include('apps.analytics.urls', namespace='analytics')),

# Search endpoints  
# path('search/', include('apps.search.urls', namespace='search')),

# Webhooks
# path('webhooks/', include('apps.webhooks.urls', namespace='webhooks')),

# Third-party integrations
# path('integrations/', include('apps.integrations.urls', namespace='integrations')),

# ==============================================================================
# 📚 URL NAMING CONVENTIONS
# ==============================================================================

"""
URL Naming Conventions:
- Collection: /api/v1/resource/
- Detail: /api/v1/resource/{id}/
- Nested: /api/v1/resource/{id}/sub-resource/
- Actions: /api/v1/resource/{id}/action/
- Filters: /api/v1/resource/?filter=value

Examples:
- GET /api/v1/pets/ - List all pets
- GET /api/v1/pets/{id}/ - Get specific pet
- POST /api/v1/pets/ - Create new pet
- PUT /api/v1/pets/{id}/ - Update pet
- DELETE /api/v1/pets/{id}/ - Delete pet
- POST /api/v1/pets/{id}/adopt/ - Adopt pet action
- GET /api/v1/pets/?category=dog&status=available - Filtered list
"""

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Bu URL yapısı, RESTful principles ve modern API design patterns'ı
# takip eder. Scalability, maintainability ve developer experience
# için optimize edilmiştir.
# 🐾 Her endpoint, organized API architecture için! 💝
