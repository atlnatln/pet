"""
🧪 Evcil Hayvan Platformu - Testing Settings
==============================================================================
Test ortamı kuralları - Hızlı, izole ve güvenilir testler için
Test süiteleri bu ayarlarla çalışır.
==============================================================================
"""

from .base import *
import tempfile

# ==============================================================================
# 🧪 TEST ENVIRONMENT - Test ortamı optimizasyonları
# ==============================================================================

# Test modunda debug kapalı (performans için)
DEBUG = False

# Test için SECRET_KEY - Güvenli ama sabit
SECRET_KEY = 'test-secret-key-for-testing-only-not-secure'

# Test host'ları
ALLOWED_HOSTS = ['testserver', 'localhost', '127.0.0.1']

# ==============================================================================
# 🗄️ DATABASE - Test için in-memory SQLite
# ==============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'OPTIONS': {
            'timeout': 20,
        }
    }
}

# ==============================================================================
# 🏃 CACHE - Test için dummy cache
# ==============================================================================

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# ==============================================================================
# 📧 EMAIL - Test için memory backend
# ==============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# ==============================================================================
# 🔐 PASSWORD HASHING - Test için hızlı hasher
# ==============================================================================

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',  # Hızlı ama güvensiz (sadece test için!)
]

# ==============================================================================
# 📁 MEDIA FILES - Test için temporary directory
# ==============================================================================

MEDIA_ROOT = tempfile.mkdtemp()

# ==============================================================================
# 🔄 CELERY - Test için synchronous execution
# ==============================================================================

# Celery'yi test'te senkron çalıştır
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# ==============================================================================
# 📊 LOGGING - Test için minimal logging
# ==============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'CRITICAL',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'CRITICAL',
    },
}

# ==============================================================================
# 🚫 DISABLED FEATURES - Test'te gereksiz özellikler
# ==============================================================================

# Migrations'ları hızlandır
class DisableMigrations:
    def __contains__(self, item):
        return True
    
    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# ==============================================================================
# 🎯 TEST SPECIFIC SETTINGS - Test özel ayarları
# ==============================================================================

# Platform ayarları - Test için hızlı değerler
ADOPTION_APPROVAL_REQUIRED = False
CONTENT_MODERATION_ENABLE = False
AUTO_APPROVE_CONTENT = True
MAX_PHOTOS_PER_PET = 5

# Test runner
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# ==============================================================================
# 🔧 TEST UTILITIES - Test yardımcıları
# ==============================================================================

# Faker için Türkçe locale
FAKER_LOCALE = 'tr_TR'

# Test data factory settings
FACTORY_FOR_DJANGO_MODELS = True

print("🧪 Test mode aktif - Test sevgisi başlasın! 🐾")
