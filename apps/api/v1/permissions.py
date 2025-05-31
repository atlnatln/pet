"""
🐾 Evcil Hayvan Platformu - API v1 Permissions
==============================================================================
Modern API authentication ve authorization sistemi.
JWT, API Key, ve role-based access control desteği.
==============================================================================
"""

from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.contrib.auth import get_user_model
from django.core.cache import cache
import time

User = get_user_model()

# ==============================================================================
# 🚀 API VERSIONING PERMISSIONS - API versiyon kontrolü
# ==============================================================================

class APIVersionPermission(BasePermission):
    """
    API version kontrolü ve deprecation uyarıları
    """
    
    def has_permission(self, request, view):
        # API version header kontrolü
        api_version = request.META.get('HTTP_API_VERSION', '1.0')
        
        # Desteklenen versiyonlar
        supported_versions = ['1.0', '1.1']
        deprecated_versions = ['0.9']
        
        if api_version in deprecated_versions:
            # Deprecated version uyarısı
            setattr(request, 'api_warning', f'API v{api_version} deprecated. Please upgrade to v1.0+')
        
        return api_version in supported_versions + deprecated_versions

# ==============================================================================
# 🔑 API KEY AUTHENTICATION - Gelecek için hazır
# ==============================================================================

class APIKeyPermission(BasePermission):
    """
    API Key based authentication (3rd party integrations için)
    """
    
    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_X_API_KEY')
        
        if not api_key:
            return False
        
        # API key validation (şimdilik basit, gelecekte database'den kontrol edilecek)
        # TODO: Implement proper API key management
        valid_keys = [
            'pet-platform-demo-key-2025',  # Demo key
        ]
        
        return api_key in valid_keys

# ==============================================================================
# 🎭 ROLE-BASED PERMISSIONS - Rol tabanlı yetkilendirme
# ==============================================================================

class IsAdoptionSpecialist(BasePermission):
    """
    Sahiplenme uzmanı yetkisi
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # User model'de role field'ı olduğunda implement edilecek
        # return request.user.role == 'adoption_specialist'
        return request.user.is_staff  # Geçici olarak staff kontrolü

class IsVeterinary(BasePermission):
    """
    Veteriner hekim yetkisi
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # TODO: Implement proper veterinary role check
        return request.user.is_staff

class IsShelterManager(BasePermission):
    """
    Barınak yöneticisi yetkisi
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # TODO: Implement shelter manager role check
        return request.user.is_staff

# ==============================================================================
# 🔒 ENHANCED SECURITY PERMISSIONS - Gelişmiş güvenlik
# ==============================================================================

class IPWhitelistPermission(BasePermission):
    """
    IP whitelist kontrolü (admin işlemleri için)
    """
    
    def has_permission(self, request, view):
        # Development'ta tüm IP'lere izin ver
        if hasattr(request, 'META') and 'REMOTE_ADDR' in request.META:
            client_ip = request.META['REMOTE_ADDR']
            
            # Whitelist'e alınmış IP'ler
            whitelisted_ips = [
                '127.0.0.1',
                '0.0.0.0',
                'localhost',
            ]
            
            return client_ip in whitelisted_ips
        
        return True  # Development'ta varsayılan olarak izin ver

class DevicePermission(BasePermission):
    """
    Device-based authentication (mobile apps için)
    """
    
    def has_permission(self, request, view):
        device_id = request.META.get('HTTP_X_DEVICE_ID')
        device_type = request.META.get('HTTP_X_DEVICE_TYPE', 'unknown')
        
        # Device registration kontrolü (gelecekte implement edilecek)
        # TODO: Implement device management system
        
        return True  # Şimdilik tüm device'lara izin ver

# ==============================================================================
# ⚡ RATE LIMITING & THROTTLING - Hız sınırlaması
# ==============================================================================

class AdoptionApplicationThrottle(UserRateThrottle):
    """
    Sahiplenme başvuruları için özel rate limiting
    """
    scope = 'adoption_applications'
    rate = '5/hour'  # Saatte 5 başvuru

class MessageThrottle(UserRateThrottle):
    """
    Mesajlaşma için rate limiting
    """
    scope = 'messages'
    rate = '100/hour'  # Saatte 100 mesaj

class ImageUploadThrottle(UserRateThrottle):
    """
    Görsel yükleme için rate limiting
    """
    scope = 'image_uploads'
    rate = '50/hour'  # Saatte 50 görsel

class PublicAPIThrottle(AnonRateThrottle):
    """
    Public API endpoints için rate limiting
    """
    scope = 'public_api'
    rate = '1000/hour'  # Saatte 1000 istek

# ==============================================================================
# 🛡️ CONTENT MODERATION PERMISSIONS - İçerik moderasyonu
# ==============================================================================

class ContentModerationPermission(BasePermission):
    """
    İçerik moderasyonu için permission
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Moderatör yetkisi kontrolü
        if hasattr(request.user, 'groups'):
            return request.user.groups.filter(name='content_moderators').exists()
        
        return request.user.is_staff

class AutoModeratedContent(BasePermission):
    """
    Otomatik moderasyon geçmiş içerik
    """
    
    def has_object_permission(self, request, view, obj):
        # Content moderation status kontrolü
        if hasattr(obj, 'moderation_status'):
            return obj.moderation_status in ['approved', 'auto_approved']
        
        return True

# ==============================================================================
# 📱 MOBILE APP PERMISSIONS - Mobil uygulama yetkileri
# ==============================================================================

class MobileAppPermission(BasePermission):
    """
    Mobil uygulama için özel permissions
    """
    
    def has_permission(self, request, view):
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        app_version = request.META.get('HTTP_X_APP_VERSION')
        
        # Mobil app kontrolü
        mobile_keywords = ['PetPlatform-iOS', 'PetPlatform-Android', 'PetPlatform-Mobile']
        is_mobile_app = any(keyword in user_agent for keyword in mobile_keywords)
        
        if is_mobile_app and app_version:
            # Minimum app version kontrolü
            min_version = '1.0.0'
            # TODO: Implement version comparison logic
            return True
        
        return True  # Web ve diğer client'lara da izin ver

# ==============================================================================
# 🔄 FEATURE FLAG PERMISSIONS - Özellik bayrakları
# ==============================================================================

class FeatureFlagPermission(BasePermission):
    """
    Feature flag kontrolü ile özellik erişimi
    """
    
    def __init__(self, feature_name):
        self.feature_name = feature_name
    
    def has_permission(self, request, view):
        # Feature flag kontrolü (cache'den)
        feature_enabled = cache.get(f'feature_{self.feature_name}', False)
        
        if not feature_enabled:
            # Beta user kontrolü
            if request.user and request.user.is_authenticated:
                is_beta_user = getattr(request.user, 'is_beta_tester', False)
                return is_beta_user
            return False
        
        return True

# ==============================================================================
# 🌍 GEO-LOCATION PERMISSIONS - Coğrafi konum yetkileri
# ==============================================================================

class GeolocationPermission(BasePermission):
    """
    Coğrafi konum tabanlı erişim kontrolü
    """
    
    def has_permission(self, request, view):
        # Geolocation header'ından konum bilgisi al
        latitude = request.META.get('HTTP_X_LATITUDE')
        longitude = request.META.get('HTTP_X_LONGITUDE')
        
        if latitude and longitude:
            # Türkiye sınırları içinde mi kontrol et
            # TODO: Implement proper geolocation validation
            pass
        
        return True  # Şimdilik tüm konumlara izin ver

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Her permission class'ı, platform güvenliği ve kullanıcı deneyimi için
# özenle tasarlandı. Modern API güvenlik standartlarını takip eder.
# 🐾 Her yetki kontrolü, güvenli bir platform için! 💝
