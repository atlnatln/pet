"""
🐾 Evcil Hayvan Platformu - ASGI Configuration
==============================================================================
ASGI config for pet platform project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
==============================================================================
"""

import os
from django.core.asgi import get_asgi_application

# Set default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

# Future WebSocket routing will be added here
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack

application = django_asgi_app

# Platform message
print("🐾 ASGI application loaded for Evcil Hayvan Platformu")
