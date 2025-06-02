"""
🐾 Hayvanlar Managers
==============================================================================
Hayvan sorgulama ve yönetimi için özel manager'lar
==============================================================================
"""

from django.db import models
from django.db.models import Q, Count
from django.core.cache import cache


class HayvanQuerySet(models.QuerySet):
    """
    Hayvan QuerySet - chainable sorgular için
    """
    
    def aktif(self):
        """Aktif hayvanlar"""
        return self.filter(aktif=True)
    
    def sahiplendirme_bekleyen(self):
        """Sahiplendirme bekleyen hayvanlar"""
        return self.filter(sahiplenildi=False)
    
    def tur_ile(self, tur):
        """Belirli türdeki hayvanlar"""
        return self.filter(tur=tur)
    
    def kategori_ile(self, kategori):
        """Belirli kategorideki hayvanlar"""
        return self.filter(kategori=kategori)
    
    def sehir_ile(self, il):
        """Belirli şehirdeki hayvanlar"""
        return self.filter(il__iexact=il)
    
    def populer(self):
        """Popüler hayvanlar (en son eklenenler)"""
        return self.order_by('-created_at')
    
    def arama(self, query):
        """Hayvan arama"""
        if not query:
            return self
        
        return self.filter(
            Q(ad__icontains=query) |
            Q(aciklama__icontains=query) |
            Q(irk__ad__icontains=query) |
            Q(kategori__ad__icontains=query)
        )


class HayvanManager(models.Manager):
    """
    Hayvan Manager - kompleks işlemler için
    """
    
    def get_queryset(self):
        return HayvanQuerySet(self.model, using=self._db)
    
    def aktif_hayvanlar(self):
        """Aktif hayvanları getir"""
        return self.get_queryset().aktif()
    
    def sahiplendirme_bekleyen(self):
        """Sahiplendirme bekleyen hayvanlar"""
        return self.aktif_hayvanlar().sahiplendirme_bekleyen()
    
    def populer_hayvanlar(self, limit=10):
        """En popüler hayvanlar"""
        cache_key = f"hayvanlar:populer:{limit}"
        hayvanlar = cache.get(cache_key)
        
        if hayvanlar is None:
            hayvanlar = list(
                self.sahiplendirme_bekleyen()
                .populer()[:limit]
                .values('id', 'ad', 'slug', 'tur')
            )
            cache.set(cache_key, hayvanlar, 1800)  # 30 dakika cache
        
        return hayvanlar
    
    def son_hayvanlar(self, limit=10):
        """Son eklenen hayvanlar"""
        return self.sahiplendirme_bekleyen().populer()[:limit]
    
    def hayvan_arama(self, query, filters=None):
        """Gelişmiş hayvan arama"""
        queryset = self.aktif_hayvanlar().arama(query)
        
        if filters:
            if filters.get('tur'):
                queryset = queryset.tur_ile(filters['tur'])
            
            if filters.get('kategori'):
                queryset = queryset.kategori_ile(filters['kategori'])
            
            if filters.get('il'):
                queryset = queryset.sehir_ile(filters['il'])
        
        return queryset.order_by('-created_at')
