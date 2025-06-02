"""
🐾 Ortak Pagination Sınıfları
==============================================================================
Platform genelindeki sayfalama ayarları
==============================================================================
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    """
    Platform standart sayfalama
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'page_size': self.page_size,
            'results': data
        })


class LargePagination(PageNumberPagination):
    """
    Büyük listeler için sayfalama
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200


class SmallPagination(PageNumberPagination):
    """
    Küçük listeler için sayfalama
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50