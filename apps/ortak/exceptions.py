"""
🐾 Evcil Hayvan Platformu - Ortak Exception'lar
==============================================================================
Platform genelinde kullanılacak özel exception sınıfları
==============================================================================
"""

from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

# ==============================================================================
# 🚨 CUSTOM EXCEPTIONS - Özel hata sınıfları
# ==============================================================================

class PlatformBaseException(Exception):
    """
    Platform için temel exception sınıfı
    """
    default_message = "Bir hata oluştu"
    default_code = "PLATFORM_ERROR"
    
    def __init__(self, message=None, code=None, extra_data=None):
        self.message = message or self.default_message
        self.code = code or self.default_code
        self.extra_data = extra_data or {}
        super().__init__(self.message)

class PetValidationError(PlatformBaseException):
    """
    Hayvan validasyonu hataları
    """
    default_message = "Hayvan bilgileri geçersiz"
    default_code = "PET_VALIDATION_ERROR"

class AdoptionApplicationError(PlatformBaseException):
    """
    Sahiplenme başvurusu hataları
    """
    default_message = "Sahiplenme başvurusu işleminde hata"
    default_code = "ADOPTION_APPLICATION_ERROR"

class UserPermissionError(PlatformBaseException):
    """
    Kullanıcı yetki hataları
    """
    default_message = "Bu işlem için yetkiniz yok"
    default_code = "USER_PERMISSION_ERROR"

class FileUploadError(PlatformBaseException):
    """
    Dosya yükleme hataları
    """
    default_message = "Dosya yükleme başarısız"
    default_code = "FILE_UPLOAD_ERROR"

class ContentModerationError(PlatformBaseException):
    """
    İçerik moderasyonu hataları
    """
    default_message = "İçerik moderasyon kurallarına aykırı"
    default_code = "CONTENT_MODERATION_ERROR"

class RateLimitExceededError(PlatformBaseException):
    """
    Rate limit aşımı hataları
    """
    default_message = "İstek limitinizi aştınız, lütfen bekleyin"
    default_code = "RATE_LIMIT_EXCEEDED"

# ==============================================================================
# 🛠️ EXCEPTION HANDLERS - Hata yakalayıcıları
# ==============================================================================

def custom_exception_handler(exc, context):
    """
    Platform için özel exception handler
    """
    
    # REST framework'ün default handler'ını çağır
    response = exception_handler(exc, context)
    
    # Custom response format
    if response is not None:
        custom_response_data = {
            'success': False,
            'error': {
                'code': getattr(exc, 'code', 'UNKNOWN_ERROR'),
                'message': str(exc),
                'details': response.data if hasattr(response, 'data') else None,
                'timestamp': context.get('request').META.get('HTTP_DATE'),
            },
            'meta': {
                'request_path': context.get('request').path,
                'request_method': context.get('request').method,
                'user': str(context.get('request').user) if hasattr(context.get('request'), 'user') else 'anonymous',
            }
        }
        
        # Log the error
        logger.error(
            f"API Error: {exc} - "
            f"Path: {context.get('request').path} - "
            f"User: {context.get('request').user if hasattr(context.get('request'), 'user') else 'anonymous'}"
        )
        
        response.data = custom_response_data
    
    return response

def handle_platform_exception(exc, request=None):
    """
    Platform exception'larını handle et
    """
    
    if isinstance(exc, PlatformBaseException):
        logger.warning(f"Platform Exception: {exc.code} - {exc.message}")
        
        return {
            'success': False,
            'error': {
                'code': exc.code,
                'message': exc.message,
                'extra_data': exc.extra_data,
            }
        }
    
    # Diğer exception'lar için default handling
    logger.error(f"Unhandled Exception: {exc}")
    return {
        'success': False,
        'error': {
            'code': 'INTERNAL_ERROR',
            'message': 'Beklenmeyen bir hata oluştu',
        }
    }

# ==============================================================================
# 🔧 VALIDATION HELPERS - Validasyon yardımcıları
# ==============================================================================

def validate_or_raise(condition, exception_class, message=None, **kwargs):
    """
    Condition false ise exception fırlat
    """
    if not condition:
        raise exception_class(message, **kwargs)

def safe_execute(func, default=None, exception_class=PlatformBaseException):
    """
    Güvenli fonksiyon çalıştırma
    """
    try:
        return func()
    except Exception as e:
        logger.error(f"Safe execute failed: {e}")
        if isinstance(e, PlatformBaseException):
            raise e
        raise exception_class(f"İşlem başarısız: {str(e)}")

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Bu exception handler'lar, platform genelinde tutarlı hata yönetimi sağlar.
# Her hata loglanır ve kullanıcı dostu mesajlar döner.
# 🐾 Her exception, daha iyi kullanıcı deneyimi için!
