"""
🏷️ Etiket Managers
==============================================================================
Etiket sorgulama ve yönetimi için özel manager'lar
==============================================================================
"""

from django.db import models
from django.db.models import Count, Q
from django.core.cache import cache
from django.utils import timezone


class EtiketQuerySet(models.QuerySet):
    """
    Etiket QuerySet - chainable sorgular için
    """
    
    def aktif(self):
        """Aktif etiketler"""
        return self.filter(aktif=True, onay_bekliyor=False)
    
    def onay_bekleyen(self):
        """Onay bekleyen etiketler"""
        return self.filter(onay_bekliyor=True)
    
    def populer(self):
        """Popüler etiketler"""
        return self.filter(populer=True)
    
    def kategori_ile(self, kategori):
        """Belirli kategorideki etiketler"""
        return self.filter(kategori=kategori)
    
    def kullanim_sirali(self):
        """Kullanım sayısına göre sıralı"""
        return self.order_by('-kullanim_sayisi', '-populer', 'ad')
    
    def arama(self, query):
        """Etiket arama"""
        if not query:
            return self
        
        return self.filter(
            Q(ad__icontains=query) |
            Q(aciklama__icontains=query)
        )
    
    def benzer_etiketler(self, etiket_adi, limit=5):
        """Benzer etiketleri bulma"""
        return self.filter(
            Q(ad__icontains=etiket_adi) |
            Q(aciklama__icontains=etiket_adi)
        ).exclude(ad=etiket_adi)[:limit]


class EtiketManager(models.Manager):
    """
    Etiket Manager - kompleks işlemler için
    """
    
    def get_queryset(self):
        return EtiketQuerySet(self.model, using=self._db)
    
    def aktif_etiketler(self):
        """Aktif etiketleri getir"""
        return self.get_queryset().aktif()
    
    def populer_etiketler(self, limit=20):
        """En popüler etiketler"""
        cache_key = f"etiketler:populer:{limit}"
        etiketler = cache.get(cache_key)
        
        if etiketler is None:
            etiketler = list(
                self.aktif_etiketler()
                .populer()
                .kullanim_sirali()[:limit]
                .values('id', 'ad', 'slug', 'kullanim_sayisi', 'kategori__ad')
            )
            cache.set(cache_key, etiketler, 1800)  # 30 dakika cache
        
        return etiketler
    
    def kategoriye_gore_etiketler(self):
        """Kategoriye göre gruplanmış etiketler"""
        cache_key = "etiketler:kategoriye_gore"
        gruplar = cache.get(cache_key)
        
        if gruplar is None:
            from .models import EtiketKategori
            
            kategoriler = EtiketKategori.objects.filter(aktif=True).prefetch_related(
                'etiketler__aktif_etiketler'
            )
            
            gruplar = {}
            for kategori in kategoriler:
                gruplar[kategori.slug] = {
                    'kategori': {
                        'id': kategori.id,
                        'ad': kategori.ad,
                        'slug': kategori.slug,
                        'renk_kodu': kategori.renk_kodu,
                        'ikon_adi': kategori.ikon_adi
                    },
                    'etiketler': list(
                        kategori.etiketler.aktif()
                        .kullanim_sirali()
                        .values('id', 'ad', 'slug', 'kullanim_sayisi')
                    )
                }
            
            cache.set(cache_key, gruplar, 3600)  # 1 saat cache
        
        return gruplar
    
    def etiket_ara_veya_olustur(self, etiket_adi, kullanici=None):
        """
        Etiket ara, bulamazsan oluştur
        Kullanıcı tarafından önerilen etiketler için
        """
        # Normalize et
        etiket_adi = etiket_adi.strip().lower().title()
        
        # Önce var olanı ara
        try:
            return self.aktif_etiketler().get(ad__iexact=etiket_adi), False
        except self.model.DoesNotExist:
            pass
        
        # Bulamazsa oluştur (onay bekler durumda)
        etiket = self.model.objects.create(
            ad=etiket_adi,
            onay_bekliyor=True,
            aktif=False  # Önce pasif olarak oluştur
        )
        
        return etiket, True
    
    def benzer_etiket_onerisi(self, query, limit=5):
        """Yazarken etiket önerisi"""
        if len(query) < 2:
            return []
        
        return list(
            self.aktif_etiketler()
            .arama(query)
            .kullanim_sirali()[:limit]
            .values('id', 'ad', 'slug')
        )
    
    def istatistikleri_guncelle(self):
        """Tüm etiketlerin kullanım istatistiklerini güncelle"""
        try:
            from apps.ilanlar.models import Ilan
            
            # Her etiket için ilan sayısını hesapla
            etiketler = self.all()
            for etiket in etiketler:
                ilan_sayisi = etiket.ilanlar.filter(aktif=True).count()
                if etiket.kullanim_sayisi != ilan_sayisi:
                    etiket.kullanim_sayisi = ilan_sayisi
                    etiket.save(update_fields=['kullanim_sayisi'])
            
            # Cache temizle
            cache.delete_many([
                "etiketler:populer:20",
                "etiketler:kategoriye_gore"
            ])
                    
        except ImportError:
            # İlanlar modeli henüz yoksa
            pass
    
    def slug_ile_getir(self, slug):
        """Slug ile etiket getir"""
        try:
            return self.aktif_etiketler().get(slug=slug)
        except self.model.DoesNotExist:
            return None

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Bu manager'lar, etiket sisteminin performansını ve kullanılabilirliğini artırır.
# Cache stratejileri ile hızlı erişim, akıllı arama ile kullanıcı dostu deneyim.
# 🏷️ Her sorgu, etiketlerin hikayesini daha verimli anlatır!
