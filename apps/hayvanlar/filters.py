"""
🐾 Evcil Hayvan Platformu - Hayvan Filtreleme
==============================================================================
API filtreleme ve arama işlevleri
==============================================================================
"""

from django_filters import rest_framework as filters
from django.utils.translation import gettext_lazy as _
from .models import Hayvan


class HayvanFilter(filters.FilterSet):
    """
    Hayvan modeli için API filtreleri
    """
    # Alan filtreleri
    tur = filters.CharFilter(lookup_expr='exact')
    irk = filters.CharFilter(field_name='irk__id', lookup_expr='exact')
    cinsiyet = filters.CharFilter(lookup_expr='exact')
    yas = filters.CharFilter(lookup_expr='exact')
    boyut = filters.CharFilter(lookup_expr='exact')
    il = filters.CharFilter(lookup_expr='iexact')
    ilce = filters.CharFilter(lookup_expr='icontains')
    
    # Boolean filtreleri
    kisirlastirilmis = filters.BooleanFilter()
    asilar_tamam = filters.BooleanFilter()
    mikrocipli = filters.BooleanFilter()
    sahiplenildi = filters.BooleanFilter()
    
    # Karakter özellikleri filtresi
    karakter = filters.CharFilter(method='filter_karakter')
    
    # Arama filtresi
    search = filters.CharFilter(method='filter_search')
    
    class Meta:
        model = Hayvan
        fields = [
            'tur', 'kategori', 'irk', 'cinsiyet', 'yas', 'boyut',
            'kisirlastirilmis', 'asilar_tamam', 'mikrocipli', 'sahiplenildi',
            'il', 'ilce'
        ]
    
    def filter_karakter(self, queryset, name, value):
        """Karakter özelliklerine göre filtrele"""
        if not value:
            return queryset
        
        karakter_ozellikleri = value.split(',')
        for ozellik in karakter_ozellikleri:
            queryset = queryset.filter(karakter_ozellikleri__contains=[ozellik])
        
        return queryset
    
    def filter_search(self, queryset, name, value):
        """Ad, açıklama ve diğer alanlarda arama"""
        if not value:
            return queryset
        
        return queryset.filter(
            models.Q(ad__icontains=value) |
            models.Q(aciklama__icontains=value) |
            models.Q(irk__ad__icontains=value) |
            models.Q(kategori__ad__icontains=value)
        )
