"""
🐾 Evcil Hayvan Platformu - Development Settings
==============================================================================
Geliştirme ortamı için özelleştirilmiş Django ayarları.
Debug araçları ve geliştirici dostu konfigürasyonlar.
==============================================================================
"""

from .base import *

# ==============================================================================
# 🔧 DEVELOPMENT SPECIFIC SETTINGS
# ==============================================================================

DEBUG = True
ENVIRONMENT = 'development'

# Development allowed hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# ==============================================================================
# 🗄️ DEVELOPMENT DATABASE
# ==============================================================================

# SQLite for development (easy setup)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==============================================================================
# 📧 DEVELOPMENT EMAIL
# ==============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ==============================================================================
# 🔐 DEVELOPMENT SECURITY (relaxed but still secure)
# ==============================================================================

# Override production security settings for development
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# Cookie security disabled for development
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# CORS more permissive for development
CORS_ALLOW_ALL_ORIGINS = True  # Only for development!

# Development-specific apps (debug_toolbar kaldırıldı)
INSTALLED_APPS += [
    # 'debug_toolbar',  # Geçici olarak kapatıldı
]

# Development-specific middleware (debug_toolbar kaldırıldı)
MIDDLEWARE += [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',  # Geçici olarak kapatıldı
]

# Debug Toolbar Settings (Geçici olarak kapatıldı)
# INTERNAL_IPS = [
#     '127.0.0.1',
#     'localhost',
# ]

# ==============================================================================
# 🌐 DEVELOPMENT CORS (permissive)
# ==============================================================================

CORS_ALLOW_ALL_ORIGINS = True  # Only for development!

# ==============================================================================
# 📝 DEVELOPMENT LOGGING (verbose)
# ==============================================================================

LOGGING['handlers']['console']['level'] = 'DEBUG'
LOGGING['root']['level'] = 'DEBUG'

# ==============================================================================
# 💝 DEVELOPMENT MESSAGE
# ==============================================================================

print("""
🐾 ===============================================
   Development Settings Loaded
===============================================

🔧 Debug Mode: ACTIVE
🗄️ Database: SQLite (development)
📧 Email: Console Backend
🌐 CORS: Permissive (all origins)

💝 Geliştirme ortamı hazır!
===============================================
""")
