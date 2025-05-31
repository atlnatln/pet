"""
🚀 Evcil Hayvan Platformu - Production Settings
==============================================================================
Savaş meydanı ayarları - Güvenlik, performans ve ölçeklenebilirlik odaklı
Her ayar production trafiği için optimize edilmiştir.
==============================================================================
"""

from .base import *
from decouple import config
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

# ==============================================================================
# 🛡️ GÜVENLİK - Production security hardening
# ==============================================================================

# Debug KAPATILMALI!
DEBUG = False

# Strict host kontrolü
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# HTTPS enforcement
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Secure cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ==============================================================================
# 📊 ERROR TRACKING - Sentry integration
# ==============================================================================

SENTRY_DSN = config('SENTRY_DSN', default='')
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(auto_enabling=True),
            CeleryIntegration(monitor_beat_tasks=True),
        ],
        traces_sample_rate=0.1,
        send_default_pii=False,
        environment=config('ENVIRONMENT', default='production'),
    )

# ==============================================================================
# 📧 EMAIL - Production SMTP
# ==============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# ==============================================================================
# 🏃 CACHE - Production Redis configuration
# ==============================================================================

# Redis cache with connection pooling
CACHES['default'].update({
    'OPTIONS': {
        'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        'IGNORE_EXCEPTIONS': True,
        'CONNECTION_POOL_KWARGS': {
            'max_connections': 50,
            'retry_on_timeout': True,
        }
    },
    'TIMEOUT': 300,
})

# ==============================================================================
# 📁 STATIC & MEDIA - Cloud storage
# ==============================================================================

# AWS S3 static files storage
if config('AWS_ACCESS_KEY_ID', default=''):
    # S3 configuration
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='eu-west-1')
    AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN', default='')
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    
    # Storage backends
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

# ==============================================================================
# 🐘 DATABASE - Production optimizations
# ==============================================================================

# Connection pooling
DATABASES['default'].update({
    'CONN_MAX_AGE': 60,
    'CONN_HEALTH_CHECKS': True,
    'OPTIONS': {
        'MAX_CONNS': 20,
        'charset': 'utf8',
    }
})

# ==============================================================================
# 📊 LOGGING - Production logging
# ==============================================================================

LOGGING.update({
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/pet-platform/django.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'mail_admins'],
            'level': 'WARNING',
            'propagate': False,
        },
        'apps': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
})

# ==============================================================================
# 🔄 CELERY - Production task queue
# ==============================================================================

# Celery optimizations
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_ACKS_LATE = True
CELERY_WORKER_MAX_TASKS_PER_CHILD = 1000

# ==============================================================================
# ⚡ PERFORMANCE - Production optimizations
# ==============================================================================

# Template caching
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]

# ==============================================================================
# 🎯 RATE LIMITING - Production protection
# ==============================================================================

REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'].update({
    'anon': '300/hour',
    'user': '3000/hour',
    'login': '5/min',
    'register': '3/hour',
})

# ==============================================================================
# 🚨 ADMIN SECURITY - Admin panel protection
# ==============================================================================

ADMINS = [
    ('Platform Admin', config('ADMIN_EMAIL', default='admin@evcilhayvanplatformu.com')),
]
MANAGERS = ADMINS

# ==============================================================================
# 🔐 CONTENT SECURITY POLICY
# ==============================================================================

CSP_DEFAULT_SRC = ["'self'"]
CSP_SCRIPT_SRC = ["'self'", "'unsafe-inline'"]
CSP_STYLE_SRC = ["'self'", "'unsafe-inline'"]
CSP_IMG_SRC = ["'self'", "data:", "https:"]
CSP_FONT_SRC = ["'self'", "https:"]

print("🚀 Production mode aktif - Platform canlıda! 🐾")
