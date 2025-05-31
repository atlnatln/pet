"""
🐾 Custom API Exception Handlers
==============================================================================
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """Custom exception handler for API endpoints"""
    
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'success': False,
            'error': {
                'code': response.status_code,
                'message': 'An error occurred',
                'details': response.data
            },
            'meta': {
                'timestamp': context['request'].META.get('HTTP_DATE'),
                'path': context['request'].path,
            }
        }
        
        # Log the error
        logger.error(f"API Error: {exc} - Path: {context['request'].path}")
        
        response.data = custom_response_data
    
    return response
