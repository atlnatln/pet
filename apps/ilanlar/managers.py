"""
📢 İlanlar Managers
==============================================================================
İlan sorgulama ve yönetimi için özel manager'lar
==============================================================================
"""

from django.db import models
from django.db.models import Q, Count
from django.utils import timezone
from django.core.cache import cache


class IlanQuerySet(models.QuerySet):
    """İlan QuerySet - chainable sorgular için"""
    
    def aktif(self):
        """Aktif ilanlar"""
        return self.filter(durum='aktif')
    
    def yayin_surecinde(self):
        """Yayın sürecindeki ilanlar"""
        now = timezone.now()
        return self.filter(
            yayinlanma_tarihi__lte=now,
            bitis_tarihi__gte=now
        )
    
    def acil(self):
        """Acil ilanlar"""
        return self.filter(acil=True)
    
    def ucretsiz(self):
        """Ücretsiz ilanlar"""
        return self.filter(ucretsiz=True)
    
    def sahiplendirme(self):
        """Sahiplendirme ilanları"""
        return self.filter(ilan_turu='sahiplendirme')
    
    def kayip(self):
        """Kayıp ilanları"""
        return self.filter(ilan_turu='kayip')
    
    def bulundu(self):
        """Bulundu ilanları"""
        return self.filter(ilan_turu='bulundu')
    
    def il_ile(self, il):
        """Belirli ildeki ilanlar"""
        return self.filter(il__iexact=il)
    
    def arama(self, query):
        """İlan arama"""
        if not query:
            return self
        
        return self.filter(
            Q(baslik__icontains=query) |
            Q(aciklama__icontains=query) |
            Q(hayvan__ad__icontains=query) |
            Q(ilan_veren_adi__icontains=query)
        )


class IlanManager(models.Manager):
    """İlan Manager - kompleks işlemler için"""
    
    def get_queryset(self):
        return IlanQuerySet(self.model, using=self._db)
    
    def aktif_ilanlar(self):
        """Aktif ilanları getir"""
        return self.get_queryset().aktif().yayin_surecinde()
    
    def acil_ilanlar(self, limit=10):
        """Acil ilanlar"""
        return self.aktif_ilanlar().acil().order_by('-yayinlanma_tarihi')[:limit]
    
    def son_ilanlar(self, limit=10):
        """Son ilanlar"""
        return self.aktif_ilanlar().order_by('-yayinlanma_tarihi')[:limit]
    
    def populer_ilanlar(self, limit=10):
        """Popüler ilanlar (en çok görüntülenen)"""
        return self.aktif_ilanlar().order_by('-goruntulenme_sayisi')[:limit]
    
    def il_istatistikleri(self):
        """İl bazında ilan istatistikleri"""
        cache_key = "ilanlar:il_istatistikleri"
        stats = cache.get(cache_key)
        
        if stats is None:
            stats = dict(
                self.aktif_ilanlar()
                .values('il')
                .annotate(count=Count('id'))
                .values_list('il', 'count')
            )
            cache.set(cache_key, stats, 1800)  # 30 dakika
        
        return stats
    
    def ilan_turu_istatistikleri(self):
        """İlan türü istatistikleri"""
        return dict(
            self.aktif_ilanlar()
            .values('ilan_turu')
            .annotate(count=Count('id'))
            .values_list('ilan_turu', 'count')
        )
