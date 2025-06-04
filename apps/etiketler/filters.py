"""
🏷️ Evcil Hayvan Platformu - Etiketler Filtreleri
==============================================================================
API için etiket filtreleme sınıfları
==============================================================================
"""

import django_filters
from django.utils.translation import gettext_lazy as _
from django.db.models import Count

from .models import Etiket


class EtiketFilter(django_filters.FilterSet):
    """Etiket modeli için filtreler"""
    ad = django_filters.CharFilter(lookup_expr='icontains', label=_("Etiket Adı"))
    harf = django_filters.CharFilter(method='filter_harf_ile_baslayan', label=_("Başlangıç Harfi"))
    min_kullanim = django_filters.NumberFilter(method='filter_min_kullanim', label=_("Min Kullanım"))
    olusturma_tarihi_baslangic = django_filters.DateFilter(
        field_name='olusturma_tarihi', 
        lookup_expr='gte',
        label=_("Oluşturulma Tarihi (Başlangıç)")
    )
    olusturma_tarihi_bitis = django_filters.DateFilter(
        field_name='olusturma_tarihi', 
        lookup_expr='lte',
        label=_("Oluşturulma Tarihi (Bitiş)")
    )
    
    class Meta:
        model = Etiket
        fields = {
            'aktif': ['exact'],
            'renk_kodu': ['exact'],
            'ikon': ['icontains'],
        }
        
    def filter_harf_ile_baslayan(self, queryset, name, value):
        """Belirli bir harfle başlayan etiketleri filtrele"""
        if value:
            # Sadece ilk harfi al
            ilk_harf = value[0]
            return queryset.filter(ad__istartswith=ilk_harf)
        return queryset
        
    def filter_min_kullanim(self, queryset, name, value):
        """Minimum kullanım sayısına göre filtrele"""
        if value is not None:
            # Hayvan ve İlanlar koleksiyonlarındaki toplam kullanım sayısı
            kullanim_queryset = queryset.annotate(
                toplam_kullanim=Count('hayvanlar', distinct=True) + Count('ilanlar', distinct=True)
            )
            return kullanim_queryset.filter(toplam_kullanim__gte=value)
        return queryset
