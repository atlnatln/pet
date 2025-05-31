"""
🐾 Evcil Hayvan Platformu - API v1 Serializers
==============================================================================
Ortak serializer'lar, validation mixins ve standardize response formatları.
Consistent API responses ve comprehensive validation sağlar.
==============================================================================
"""

from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from datetime import datetime
import uuid

# ==============================================================================
# 📄 PAGINATION SERIALIZERS - Sayfalama
# ==============================================================================

class StandardPagination(PageNumberPagination):
    """
    Platform standardı pagination
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'count': self.page.paginator.count,
                'current_page': self.page.number,
                'total_pages': self.page.paginator.num_pages,
                'page_size': self.page_size,
                'has_next': self.page.has_next(),
                'has_previous': self.page.has_previous(),
                'next_url': self.get_next_link(),
                'previous_url': self.get_previous_link(),
            },
            'results': data,
            'meta': {
                'timestamp': timezone.now().isoformat(),
                'api_version': '1.0',
                'platform': 'Evcil Hayvan Platformu'
            }
        })

class PaginationSerializer(serializers.Serializer):
    """
    Pagination metadata serializer
    """
    count = serializers.IntegerField()
    current_page = serializers.IntegerField()
    total_pages = serializers.IntegerField()
    page_size = serializers.IntegerField()
    has_next = serializers.BooleanField()
    has_previous = serializers.BooleanField()
    next_url = serializers.URLField(allow_null=True)
    previous_url = serializers.URLField(allow_null=True)

# ==============================================================================
# 🔧 COMMON FIELD MIXINS - Ortak alan mixins
# ==============================================================================

class TimestampedSerializerMixin:
    """
    Timestamped model'lar için ortak alanlar
    """
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Human-readable zaman formatı ekle
        if hasattr(instance, 'created_at') and instance.created_at:
            data['created_at_human'] = instance.get_age_display()
        
        return data

class UUIDSerializerMixin:
    """
    UUID model'lar için ortak alanlar
    """
    id = serializers.UUIDField(read_only=True)
    short_id = serializers.SerializerMethodField()
    
    def get_short_id(self, obj):
        """Kısa UUID formatı"""
        if hasattr(obj, 'get_short_id'):
            return obj.get_short_id()
        return str(obj.id).split('-')[0] if obj.id else None

class OwnershipSerializerMixin:
    """
    Ownership model'lar için ortak alanlar
    """
    is_owner = serializers.SerializerMethodField()
    
    def get_is_owner(self, obj):
        """Kullanıcının sahip olup olmadığını döner"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.is_owner(request.user) if hasattr(obj, 'is_owner') else False
        return False

# ==============================================================================
# 📝 RESPONSE SERIALIZERS - Standart response formatları
# ==============================================================================

class StandardResponseSerializer(serializers.Serializer):
    """
    Standart API response formatı
    """
    success = serializers.BooleanField(default=True)
    message = serializers.CharField(max_length=500)
    data = serializers.JSONField(required=False)
    errors = serializers.JSONField(required=False)
    meta = serializers.JSONField(required=False)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Meta bilgileri ekle
        if 'meta' not in data or not data['meta']:
            data['meta'] = {
                'timestamp': timezone.now().isoformat(),
                'api_version': '1.0',
                'request_id': str(uuid.uuid4()),
            }
        
        return data

class ErrorResponseSerializer(serializers.Serializer):
    """
    Hata response formatı
    """
    success = serializers.BooleanField(default=False)
    error_code = serializers.CharField(max_length=100)
    error_message = serializers.CharField(max_length=1000)
    field_errors = serializers.JSONField(required=False)
    details = serializers.JSONField(required=False)
    meta = serializers.JSONField(required=False)

class SuccessResponseSerializer(serializers.Serializer):
    """
    Başarılı işlem response formatı
    """
    success = serializers.BooleanField(default=True)
    message = serializers.CharField(max_length=500)
    data = serializers.JSONField(required=False)

# ==============================================================================
# 🔍 VALIDATION MIXINS - Doğrulama mixins
# ==============================================================================

class TurkishPhoneValidationMixin:
    """
    Türk telefon numarası validasyonu
    """
    
    def validate_phone(self, value):
        """Telefon numarası validasyonu"""
        from apps.ortak.validators import validate_turkish_phone
        
        try:
            return validate_turkish_phone(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(str(e))

class ImageValidationMixin:
    """
    Görsel validasyonu mixin
    """
    
    def validate_image(self, value):
        """Görsel validasyonu"""
        from apps.ortak.validators import validate_pet_image
        
        try:
            validate_pet_image(value)
            return value
        except DjangoValidationError as e:
            raise serializers.ValidationError(str(e))

class ContentModerationMixin:
    """
    İçerik moderasyonu mixin
    """
    
    def validate_content_fields(self, attrs):
        """İçerik alanlarını modere et"""
        from apps.ortak.validators import validate_content_appropriateness
        
        # Modere edilecek alanlar
        content_fields = ['title', 'description', 'content', 'message']
        
        for field_name in content_fields:
            if field_name in attrs:
                try:
                    validate_content_appropriateness(attrs[field_name])
                except DjangoValidationError as e:
                    raise serializers.ValidationError({field_name: str(e)})
        
        return attrs

# ==============================================================================
# 🌐 API METADATA SERIALIZERS - API meta bilgileri
# ==============================================================================

class APIMetadataSerializer(serializers.Serializer):
    """
    API meta bilgi serializer'ı
    """
    version = serializers.CharField(default='1.0')
    timestamp = serializers.DateTimeField(default=timezone.now)
    request_id = serializers.UUIDField(default=uuid.uuid4)
    user_id = serializers.SerializerMethodField()
    user_role = serializers.SerializerMethodField()
    
    def get_user_id(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return str(request.user.id) if hasattr(request.user, 'id') else None
        return None
    
    def get_user_role(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return getattr(request.user, 'role', 'user')
        return 'anonymous'

class HealthCheckSerializer(serializers.Serializer):
    """
    Health check response serializer
    """
    status = serializers.CharField(default='healthy')
    message = serializers.CharField()
    version = serializers.CharField()
    environment = serializers.CharField()
    timestamp = serializers.DateTimeField()
    django_version = serializers.CharField()
    services = serializers.JSONField(required=False)

# ==============================================================================
# 📊 ANALYTICS SERIALIZERS - Analitik veri
# ==============================================================================

class AnalyticsSerializerMixin:
    """
    Analytics data için mixin
    """
    view_count = serializers.IntegerField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    share_count = serializers.IntegerField(read_only=True)
    engagement_score = serializers.SerializerMethodField()
    
    def get_engagement_score(self, obj):
        """Engagement score hesaplama"""
        if hasattr(obj, 'view_count') and hasattr(obj, 'like_count'):
            views = obj.view_count or 0
            likes = obj.like_count or 0
            shares = getattr(obj, 'share_count', 0) or 0
            
            if views > 0:
                return round((likes + shares * 2) / views * 100, 2)
        
        return 0.0

# ==============================================================================
# 🔒 PERMISSION CONTEXT SERIALIZERS - Yetki konteksti
# ==============================================================================

class PermissionContextSerializer(serializers.Serializer):
    """
    Kullanıcı yetki konteksti
    """
    can_edit = serializers.SerializerMethodField()
    can_delete = serializers.SerializerMethodField()
    can_moderate = serializers.SerializerMethodField()
    can_report = serializers.SerializerMethodField()
    
    def get_can_edit(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return (hasattr(obj, 'is_owner') and obj.is_owner(request.user)) or request.user.is_staff
        return False
    
    def get_can_delete(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return (hasattr(obj, 'is_owner') and obj.is_owner(request.user)) or request.user.is_staff
        return False
    
    def get_can_moderate(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.is_staff  # TODO: Implement proper moderation permissions
        return False
    
    def get_can_report(self, obj):
        request = self.context.get('request')
        return request and request.user.is_authenticated

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Her serializer, API consistency ve developer experience için tasarlandı.
# Standardize response formatları, comprehensive validation ve 
# user-friendly error handling sağlar.
# 🐾 Her API response, güvenli veri iletimi için! 💝
