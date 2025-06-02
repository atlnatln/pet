"""
📢 İlanlar Filtreleme
==============================================================================
İlan API filtreleme ve arama işlevleri
==============================================================================
"""

from django_filters import rest_framework as filters
from django.utils.translation import gettext_lazy as _
from .models import Ilan


class IlanFilter(filters.FilterSet):
    """İlan filtreleri"""
    
    # Alan filtreleri
    ilan_turu = filters.CharFilter(lookup_expr='exact')
    durum = filters.CharFilter(lookup_expr='exact')
    il = filters.CharFilter(lookup_expr='iexact')
    ilce = filters.CharFilter(lookup_expr='icontains')
    
    # Boolean filtreleri
    acil = filters.BooleanFilter()
    ucretsiz = filters.BooleanFilter()
    
    # Fiyat aralığı
    min_fiyat = filters.NumberFilter(field_name='fiyat', lookup_expr='gte')
    max_fiyat = filters.NumberFilter(field_name='fiyat', lookup_expr='lte')
    
    # Tarih filtreleri
    yayinlanma_baslangic = filters.DateFilter(field_name='yayinlanma_tarihi', lookup_expr='gte')
    yayinlanma_bitis = filters.DateFilter(field_name='yayinlanma_tarihi', lookup_expr='lte')
    
    # Hayvan filtreleri
    hayvan_tur = filters.CharFilter(field_name='hayvan__tur', lookup_expr='exact')
    hayvan_cinsiyet = filters.CharFilter(field_name='hayvan__cinsiyet', lookup_expr='exact')
    hayvan_yas = filters.CharFilter(field_name='hayvan__yas', lookup_expr='exact')
    
    # Arama
    search = filters.CharFilter(method='filter_search')
    
    class Meta:
        model = Ilan
        fields = [
            'ilan_turu', 'durum', 'il', 'ilce', 'acil', 'ucretsiz',
            'hayvan_tur', 'hayvan_cinsiyet', 'hayvan_yas'
        ]
    
    def filter_search(self, queryset, name, value):
        """Genel arama"""
        if not value:
            return queryset
        
        from django.db.models import Q
        return queryset.filter(
            Q(baslik__icontains=value) |
            Q(aciklama__icontains=value) |
            Q(hayvan__ad__icontains=value) |
            Q(ilan_veren_adi__icontains=value)
        )
