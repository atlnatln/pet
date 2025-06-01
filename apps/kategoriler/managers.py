"""
🐾 Kategori Managers
==============================================================================
Kategori sorgulama ve yönetimi için özel manager'lar
==============================================================================
"""

from django.db import models
from django.db.models import Count, Q
from django.core.cache import cache


class KategoriQuerySet(models.QuerySet):
    """
    Kategori QuerySet - chainable sorgular için
    """
    
    def aktif(self):
        """Aktif kategoriler"""
        return self.filter(aktif=True)
    
    def ana_kategoriler(self):
        """Ana kategoriler (parent=None)"""
        return self.filter(parent=None)
    
    def alt_kategoriler(self):
        """Alt kategoriler (parent!=None)"""
        return self.filter(parent__isnull=False)
    
    def pet_type_ile(self, pet_type):
        """Belirli pet type'ı ile"""
        return self.filter(pet_type=pet_type)
    
    def populer(self, limit=10):
        """En populer kategoriler"""
        return self.filter(kullanim_sayisi__gt=0).order_by('-kullanim_sayisi')[:limit]
    
    def arama(self, query):
        """Kategori arama"""
        if not query:
            return self
        
        return self.filter(
            Q(ad__icontains=query) |
            Q(aciklama__icontains=query)
        )
    
    def hiyerarshi_ile(self):
        """Kategori hiyerarşisi ile birlikte getir"""
        return self.select_related('parent').prefetch_related('alt_kategoriler')
    
    def istatistik_ile(self):
        """İstatistik bilgileri ile birlikte"""
        return self.annotate(
            alt_kategori_sayisi=Count('alt_kategoriler', filter=Q(alt_kategoriler__aktif=True))
        )


class KategoriManager(models.Manager):
    """
    Kategori Manager - kompleks işlemler için
    """
    
    def get_queryset(self):
        return KategoriQuerySet(self.model, using=self._db)
    
    def aktif_kategoriler(self):
        """Aktif kategorileri getir"""
        return self.get_queryset().aktif()
    
    def ana_kategoriler(self):
        """Ana kategorileri getir"""
        cache_key = "kategoriler:ana_kategoriler"
        kategoriler = cache.get(cache_key)
        
        if kategoriler is None:
            kategoriler = list(
                self.get_queryset()
                .aktif()
                .ana_kategoriler()
                .order_by('sira', 'ad')
                .values('id', 'ad', 'slug', 'ikon_adi', 'renk_kodu', 'aciklama', 'pet_type')
            )
            cache.set(cache_key, kategoriler, 3600)  # 1 saat cache
        
        return kategoriler
    
    def kategori_agaci(self):
        """Tüm kategori ağacını getir"""
        cache_key = "kategoriler:agac"
        agac = cache.get(cache_key)
        
        if agac is None:
            ana_kategoriler = self.get_queryset().aktif().ana_kategoriler().hiyerarshi_ile()
            
            agac = []
            for ana_kategori in ana_kategoriler:
                kategori_data = {
                    'id': ana_kategori.id,
                    'ad': ana_kategori.ad,
                    'slug': ana_kategori.slug,
                    'ikon_adi': ana_kategori.ikon_adi,
                    'renk_kodu': ana_kategori.renk_kodu,
                    'aciklama': ana_kategori.aciklama,
                    'pet_type': ana_kategori.pet_type,
                    'alt_kategoriler': []
                }
                
                # Alt kategorileri ekle
                for alt_kategori in ana_kategori.alt_kategoriler.filter(aktif=True):
                    kategori_data['alt_kategoriler'].append({
                        'id': alt_kategori.id,
                        'ad': alt_kategori.ad,
                        'slug': alt_kategori.slug,
                        'aciklama': alt_kategori.aciklama,
                        'kullanim_sayisi': alt_kategori.kullanim_sayisi,
                    })
                
                agac.append(kategori_data)
            
            cache.set(cache_key, agac, 1800)  # 30 dakika cache
        
        return agac
    
    def pet_type_kategorileri(self, pet_type):
        """Belirli pet type'ının kategorileri"""
        return (
            self.get_queryset()
            .aktif()
            .pet_type_ile(pet_type)
            .order_by('sira', 'ad')
        )
    
    def populer_kategoriler(self, limit=10):
        """En popüler kategoriler"""
        cache_key = f"kategoriler:populer:{limit}"
        kategoriler = cache.get(cache_key)
        
        if kategoriler is None:
            kategoriler = list(
                self.get_queryset()
                .aktif()
                .populer(limit)
                .values('id', 'ad', 'slug', 'kullanim_sayisi', 'ikon_adi', 'renk_kodu')
            )
            cache.set(cache_key, kategoriler, 1800)  # 30 dakika cache
        
        return kategoriler
    
    def arama_yap(self, query, limit=20):
        """Kategori arama"""
        if not query or len(query) < 2:
            return []
        
        return (
            self.get_queryset()
            .aktif()
            .arama(query)
            .order_by('-kullanim_sayisi', 'ad')[:limit]
        )
    
    def slug_ile_getir(self, slug):
        """Slug ile kategori getir"""
        try:
            return self.get_queryset().aktif().get(slug=slug)
        except self.model.DoesNotExist:
            return None
    
    def istatistikleri_guncelle(self, kategori_id):
        """Kategori kullanım istatistiklerini güncelle"""
        try:
            kategori = self.get(id=kategori_id)
            
            # Hayvan modeli ile entegrasyon eklendi
            try:
                from apps.hayvanlar.models import Hayvan
                hayvan_sayisi = Hayvan.objects.filter(kategori=kategori).count()
                kategori.kullanim_sayisi = hayvan_sayisi
                kategori.save(update_fields=['kullanim_sayisi'])
            except ImportError:
                # Hayvanlar modülü henüz import edilemiyorsa
                pass
                
            # Cache'i temizle
            cache.delete_many([
                "kategoriler:ana_kategoriler",
                "kategoriler:agac",
                f"kategoriler:populer:10"
            ])
            
        except self.model.DoesNotExist:
            pass
    
    def aktif(self):
        return self.filter(aktif=True)


class KategoriOzellikManager(models.Manager):
    """
    Kategori özellik manager'ı
    """
    
    def aktif_ozellikler(self):
        """Aktif özellikler"""
        return self.filter(aktif=True)
    
    def kategori_ozellikleri(self, kategori):
        """Belirli kategorinin özellikleri"""
        return (
            self.aktif_ozellikler()
            .filter(kategori=kategori)
            .order_by('sira', 'ad')
        )
    
    def zorunlu_ozellikler(self, kategori):
        """Kategorinin zorunlu özellikleri"""
        return (
            self.kategori_ozellikleri(kategori)
            .filter(zorunlu=True)
        )

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Bu manager'lar, kategori sisteminin verimliliğini sağlar.
# Cache stratejileri ile hızlı erişim, QuerySet'ler ile esnek sorgular.
# 🐾 Her sorgu, platformun performansı için optimize edildi!
