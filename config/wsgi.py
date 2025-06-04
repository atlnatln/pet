"""
🐾 Evcil Hayvan Platformu - WSGI Configuration
==============================================================================
WSGI config for pet platform project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
==============================================================================
"""

import os
import sys
from pathlib import Path

# Project root'u sys.path'e ekle
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# ==============================================================================
# 🔧 ENVIRONMENT SETUP - Ortam hazırlığı
# ==============================================================================

# Environment detection
environment = os.getenv('DJANGO_ENVIRONMENT', 'development').lower()  # Varsayılan olarak development kullan

# Production için settings modülü
settings_modules = {
    'development': 'config.settings.development',
    'testing': 'config.settings.testing',
    'staging': 'config.settings.production',
    'production': 'config.settings.production',
}

settings_module = settings_modules.get(environment, 'config.settings.production')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

# ==============================================================================
# 🚨 PRODUCTION VALIDATION - Production kontrolleri
# ==============================================================================

if environment == 'production':
    # Critical environment variables kontrolü
    required_vars = ['SECRET_KEY', 'DATABASE_URL', 'ALLOWED_HOSTS']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        error_msg = f"Production WSGI Error: Missing environment variables: {', '.join(missing_vars)}"
        print(error_msg, file=sys.stderr)
        
        # Logging için
        import logging
        logging.critical(error_msg)
        
        raise RuntimeError(error_msg)

# ==============================================================================
# 🚀 DJANGO APPLICATION - WSGI app oluşturma
# ==============================================================================

try:
    from django.core.wsgi import get_wsgi_application
    
    # Django setup
    application = get_wsgi_application()
    
    # Production'da başarılı startup logu
    if environment == 'production':
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"🐾 Evcil Hayvan Platformu WSGI started successfully in {environment} mode")
        
except Exception as e:
    # Startup hatası logging
    import logging
    logging.critical(f"WSGI Application startup failed: {str(e)}")
    
    # Production'da detaylı hata gösterme
    if environment != 'production':
        raise
    else:
        # Production'da güvenli hata mesajı
        print("WSGI Application failed to start. Check logs for details.", file=sys.stderr)
        sys.exit(1)

# ==============================================================================
# 🔍 WSGI MIDDLEWARE WRAPPER - Production enhancements
# ==============================================================================

class ProductionWSGIMiddleware:
    """
    Production için WSGI middleware wrapper
    Request/response monitoring ve error handling
    """
    
    def __init__(self, application):
        self.application = application
        
    def __call__(self, environ, start_response):
        # Request başlangıç zamanı
        import time
        start_time = time.time()
        
        # Request bilgileri
        method = environ.get('REQUEST_METHOD', '')
        path = environ.get('PATH_INFO', '')
        
        def custom_start_response(status, headers, exc_info=None):
            # Response zamanı hesapla
            duration = time.time() - start_time
            
            # Slow request uyarısı (>5 saniye)
            if duration > 5.0:
                import logging
                logger = logging.getLogger('performance')
                logger.warning(f"Slow request: {method} {path} took {duration:.2f}s")
            
            return start_response(status, headers, exc_info)
        
        try:
            return self.application(environ, custom_start_response)
        except Exception as e:
            # Unexpected error logging
            import logging
            logger = logging.getLogger('wsgi.error')
            logger.error(f"WSGI Error in {method} {path}: {str(e)}")
            raise

# Production'da middleware wrapper kullan
if environment == 'production':
    application = ProductionWSGIMiddleware(application)

# ==============================================================================
# 💝 PLATFORM WSGI MESSAGE
# ==============================================================================

print(f"""
🐾 ===============================================
   Evcil Hayvan Platformu WSGI Ready
===============================================

🌍 Environment: {environment.upper()}
⚙️  Settings: {settings_module}
🚀 WSGI Application: Ready to serve requests

💝 Hayvan sevgisi WSGI ile dünyaya yayılıyor!
===============================================
""")
