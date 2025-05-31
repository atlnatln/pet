"""
🐾 Kategoriler İş Mantığı Servisleri
==============================================================================
Kategori işlemlerinin merkezi iş mantığı - Her işlemin hikayesi burada
==============================================================================
"""

from typing import List, Dict, Optional, Tuple
from django.db import transaction
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .models import Kategori, KategoriOzellik, KATEGORI_HIKAYELERI
from apps.ortak.exceptions import PlatformBaseException


class KategoriService:
    """
    Kategori işlemleri için merkezi servis sınıfı
    """
    
    @staticmethod
    def kategori_agaci_olustur() -> List[Dict]:
        """
        Kategori ağacını oluştur ve cache'le
        """
        cache_key = "kategori_agaci_service"
        agac = cache.get(cache_key)
        
        if agac is None:
            agac = Kategori.objects.kategori_agaci()
            cache.set(cache_key, agac, 1800)  # 30 dakika
        
        return agac
    
    @staticmethod
    def ana_kategorileri_getir() -> List[Dict]:
        """
        Ana kategorileri hikayeli açıklamalarla getir
        """
        ana_kategoriler = Kategori.objects.ana_kategoriler()
        
        # Her kategori için hikaye ekle
        for kategori in ana_kategoriler:
            pet_type = kategori['pet_type']
            if pet_type in KATEGORI_HIKAYELERI:
                hikaye = KATEGORI_HIKAYELERI[pet_type]
                kategori.update({
                    'hikaye_baslik': hikaye['baslik'],
                    'hikaye_metin': hikaye['hikaye'],
                    'varsayilan_ikon': hikaye['ikon'],
                    'varsayilan_renk': hikaye['renk']
                })
        
        return ana_kategoriler
    
    @staticmethod
    @transaction.atomic
    def kategori_olustur(kategori_data: Dict) -> Kategori:
        """
        Yeni kategori oluştur
        """
        try:
            # Slug otomatik oluşturulacak
            kategori = Kategori.objects.create(**kategori_data)
            
            # Cache temizle
            KategoriService._cache_temizle()
            
            return kategori
            
        except Exception as e:
            raise PlatformBaseException(
                message=_("Kategori oluşturulamadı: {error}").format(error=str(e)),
                code="KATEGORI_OLUSTURMA_HATASI"
            )
    
    @staticmethod
    @transaction.atomic
    def kategori_guncelle(kategori_id: int, guncelleme_data: Dict) -> Kategori:
        """
        Kategori güncelle
        """
        try:
            kategori = Kategori.objects.get(id=kategori_id)
            
            # Güncellemeleri uygula
            for field, value in guncelleme_data.items():
                setattr(kategori, field, value)
            
            kategori.full_clean()
            kategori.save()
            
            # Cache temizle
            KategoriService._cache_temizle()
            
            return kategori
            
        except Kategori.DoesNotExist:
            raise PlatformBaseException(
                message=_("Güncellenecek kategori bulunamadı"),
                code="KATEGORI_BULUNAMADI"
            )
        except ValidationError as e:
            raise PlatformBaseException(
                message=_("Kategori güncellenemedi: {error}").format(error=str(e)),
                code="KATEGORI_GUNCELLEME_HATASI"
            )
    
    @staticmethod
    def kategori_sil(kategori_id: int) -> bool:
        """
        Kategori sil (soft delete)
        """
        try:
            kategori = Kategori.objects.get(id=kategori_id)
            
            # Alt kategorileri kontrol et
            if kategori.alt_kategoriler.filter(aktif=True).exists():
                raise PlatformBaseException(
                    message=_("Bu kategorinin aktif alt kategorileri var, silinemez"),
                    code="KATEGORI_ALT_KATEGORI_VAR"
                )
            
            # Hayvan kontrolü (hayvan modeli oluşturulduktan sonra eklenecek)
            # if kategori.hayvanlar.exists():
            #     raise PlatformBaseException(
            #         message=_("Bu kategoride hayvanlar var, silinemez"),
            #         code="KATEGORI_HAYVAN_VAR"
            #     )
            
            # Soft delete
            kategori.aktif = False
            kategori.save()
            
            # Cache temizle
            KategoriService._cache_temizle()
            
            return True
            
        except Kategori.DoesNotExist:
            raise PlatformBaseException(
                message=_("Silinecek kategori bulunamadı"),
                code="KATEGORI_BULUNAMADI"
            )
    
    @staticmethod
    def kategori_arama(arama_terimi: str, limit: int = 20) -> List[Kategori]:
        """
        Kategori arama
        """
        if not arama_terimi or len(arama_terimi) < 2:
            return []
        
        return Kategori.objects.arama_yap(arama_terimi, limit)
    
    @staticmethod
    def kategori_istatistikleri() -> Dict:
        """
        Kategori istatistiklerini hesapla
        """
        cache_key = "kategori_istatistikleri_service"
        stats = cache.get(cache_key)
        
        if stats is None:
            from django.db.models import Count
            
            stats = {
                'toplam_kategori': Kategori.objects.aktif().count(),
                'ana_kategori_sayisi': Kategori.objects.aktif().ana_kategoriler().count(),
                'alt_kategori_sayisi': Kategori.objects.aktif().alt_kategoriler().count(),
                'pet_type_dagilimi': dict(
                    Kategori.objects.aktif()
                    .values('pet_type')
                    .annotate(count=Count('id'))
                    .values_list('pet_type', 'count')
                ),
                'en_populer_5': Kategori.objects.populer_kategoriler(5)
            }
            
            cache.set(cache_key, stats, 3600)  # 1 saat
        
        return stats
    
    @staticmethod
    def kategori_ozellikleri_getir(kategori_id: int) -> List[KategoriOzellik]:
        """
        Kategorinin özelliklerini getir
        """
        try:
            kategori = Kategori.objects.get(id=kategori_id)
            return KategoriOzellik.objects.kategori_ozellikleri(kategori)
        except Kategori.DoesNotExist:
            return []
    
    @staticmethod
    @transaction.atomic
    def kategori_ozellik_ekle(kategori_id: int, ozellik_data: Dict) -> KategoriOzellik:
        """
        Kategoriye özellik ekle
        """
        try:
            kategori = Kategori.objects.get(id=kategori_id)
            ozellik_data['kategori'] = kategori
            
            ozellik = KategoriOzellik.objects.create(**ozellik_data)
            
            # Cache temizle
            KategoriService._cache_temizle()
            
            return ozellik
            
        except Kategori.DoesNotExist:
            raise PlatformBaseException(
                message=_("Kategori bulunamadı"),
                code="KATEGORI_BULUNAMADI"
            )
    
    @staticmethod
    def pet_type_kategorileri(pet_type: str) -> List[Kategori]:
        """
        Belirli pet type'ının kategorilerini getir
        """
        return Kategori.objects.pet_type_kategorileri(pet_type)
    
    @staticmethod
    def kategori_breadcrumb(kategori_id: int) -> List[Dict]:
        """
        Kategori breadcrumb yolunu getir
        """
        try:
            kategori = Kategori.objects.get(id=kategori_id)
            return kategori.get_breadcrumbs()
        except Kategori.DoesNotExist:
            return []
    
    @staticmethod
    def kategori_kullanim_guncelle(kategori_id: int):
        """
        Kategori kullanım sayısını güncelle
        """
        Kategori.objects.istatistikleri_guncelle(kategori_id)
    
    @staticmethod
    def _cache_temizle():
        """
        Kategori ile ilgili tüm cache'leri temizle
        """
        cache_keys = [
            "kategoriler:ana_kategoriler",
            "kategoriler:agac",
            "kategori_agaci_service",
            "kategori_istatistikleri_service"
        ]
        
        for key in cache_keys:
            cache.delete(key)
        
        # Pattern-based cache temizleme
        try:
            from django_redis import get_redis_connection
            conn = get_redis_connection("default")
            
            patterns = ["kategoriler:*", "kategori:*"]
            for pattern in patterns:
                keys = conn.keys(pattern)
                if keys:
                    conn.delete(*keys)
        except:
            pass


class KategoriInitializationService:
    """
    Kategori sistemi başlangıç servisi
    İlk kurulumda temel kategorileri oluşturur
    """
    
    @staticmethod
    @transaction.atomic
    def temel_kategorileri_olustur():
        """
        Platform için temel kategorileri oluştur
        """
        temel_kategoriler = [
            {
                'ad': 'Köpekler',
                'pet_type': 'dog',
                'ikon_adi': 'fa-dog',
                'renk_kodu': '#f59e0b',
                'aciklama': 'Sadakat ve dostluğun temsilcileri',
                'sira': 1
            },
            {
                'ad': 'Kediler', 
                'pet_type': 'cat',
                'ikon_adi': 'fa-cat',
                'renk_kodu': '#8b5cf6',
                'aciklama': 'Bağımsızlık ve zarafetin ustası',
                'sira': 2
            },
            {
                'ad': 'Kuşlar',
                'pet_type': 'bird',
                'ikon_adi': 'fa-dove',
                'renk_kodu': '#06b6d4',
                'aciklama': 'Özgürlüğün renkli elçileri',
                'sira': 3
            },
            {
                'ad': 'Balıklar',
                'pet_type': 'fish',
                'ikon_adi': 'fa-fish',
                'renk_kodu': '#3b82f6',
                'aciklama': 'Sessiz güzelliğin temsilcileri',
                'sira': 4
            },
            {
                'ad': 'Kemirgenler',
                'pet_type': 'rabbit',
                'ikon_adi': 'fa-rabbit',
                'renk_kodu': '#f97316',
                'aciklama': 'Minik dostların büyük kalpleri',
                'sira': 5
            },
            {
                'ad': 'Sürüngenler',
                'pet_type': 'reptile',
                'ikon_adi': 'fa-turtle',
                'renk_kodu': '#059669',
                'aciklama': 'Antik dünyanın gizemli temsilcileri',
                'sira': 6
            },
            {
                'ad': 'Egzotik Hayvanlar',
                'pet_type': 'other',
                'ikon_adi': 'fa-paw',
                'renk_kodu': '#dc2626',
                'aciklama': 'Farklılığın renkli dünyası',
                'sira': 7
            }
        ]
        
        created_count = 0
        for kategori_data in temel_kategoriler:
            kategori, created = Kategori.objects.get_or_create(
                ad=kategori_data['ad'],
                defaults=kategori_data
            )
            if created:
                created_count += 1
        
        return created_count

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Bu servisler, kategori sisteminin iş mantığını yönetir.
# Her işlem, platformun kategori hikayesinin bir parçasıdır.
# 🐾 Her servis metodu, kategorilerin yaşam döngüsünü destekler!
