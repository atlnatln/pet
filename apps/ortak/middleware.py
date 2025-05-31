"""
🐾 Evcil Hayvan Platformu - Security Middleware
==============================================================================
Custom security middleware for enhanced protection
==============================================================================
"""

import logging
import time
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from ipware import get_client_ip

logger = logging.getLogger(__name__)
User = get_user_model()

class SecurityMiddleware(MiddlewareMixin):
    """
    Enhanced security middleware for pet platform
    """
    
    def process_request(self, request):
        # Get client IP
        client_ip, is_routable = get_client_ip(request)
        request.client_ip = client_ip
        
        # Rate limiting per IP
        if self.is_rate_limited(client_ip, request):
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return HttpResponseForbidden("Rate limit exceeded")
        
        # Suspicious activity detection
        if self.detect_suspicious_activity(request):
            logger.warning(f"Suspicious activity detected from IP: {client_ip}")
            # Block but don't return error (log for investigation)
        
        return None
    
    def is_rate_limited(self, ip, request):
        """Rate limiting based on IP and endpoint"""
        
        # Different limits for different endpoints
        if '/api/v1/auth/login/' in request.path:
            limit = 5  # 5 login attempts
            window = 300  # 5 minutes
        elif '/api/v1/' in request.path:
            limit = 100  # 100 API calls
            window = 3600  # 1 hour
        else:
            limit = 200  # 200 general requests
            window = 3600  # 1 hour
        
        cache_key = f"rate_limit:{ip}:{request.path_info}"
        requests = cache.get(cache_key, 0)
        
        if requests >= limit:
            return True
        
        # Increment counter
        cache.set(cache_key, requests + 1, window)
        return False
    
    def detect_suspicious_activity(self, request):
        """Detect suspicious patterns"""
        
        suspicious_patterns = [
            # SQL injection attempts
            'union select', 'drop table', '1=1', 'script>',
            # Path traversal
            '../', '..\\', '/etc/passwd',
            # Command injection
            '; cat ', '| nc ', '&& curl'
        ]
        
        query_string = request.GET.urlencode().lower()
        post_data = str(request.POST).lower() if request.POST else ""
        
        for pattern in suspicious_patterns:
            if pattern in query_string or pattern in post_data:
                return True
        
        return False

class AuditMiddleware(MiddlewareMixin):
    """
    Audit trail middleware for sensitive operations
    """
    
    def process_request(self, request):
        # Log sensitive operations
        if self.is_sensitive_operation(request):
            self.log_operation(request)
        
        return None
    
    def is_sensitive_operation(self, request):
        """Check if operation is sensitive"""
        sensitive_paths = [
            '/admin/',
            '/api/v1/users/',
            '/api/v1/applications/',
            '/api/v1/adoptions/',
        ]
        
        return any(path in request.path for path in sensitive_paths)
    
    def log_operation(self, request):
        """Log sensitive operation"""
        logger.info(
            f"Sensitive operation: {request.method} {request.path} "
            f"by user: {getattr(request.user, 'username', 'anonymous')} "
            f"from IP: {getattr(request, 'client_ip', 'unknown')}"
        )
