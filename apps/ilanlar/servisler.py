"""
📢 İlanlar İş Mantığı Servisleri
==============================================================================
İlan işlemlerinin merkezi iş mantığı
==============================================================================
"""

from typing import List, Dict, Optional
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from apps.ortak.exceptions import PlatformBaseException
from .models import Ilan, IlanBasvuru


class IlanService:
    """
    İlan işlemleri için merkezi servis sınıfı
    """
    
    @staticmethod
    @transaction.atomic
    def ilan_olustur(ilan_data: Dict, hayvan_id: int, user=None) -> Ilan:
        """
        Yeni ilan oluştur
        """
        try:
            from apps.hayvanlar.models import Hayvan
            
            # Hayvanı bul
            hayvan = Hayvan.objects.get(id=hayvan_id, aktif=True)
            
            # İlan verilerini hazırla
            ilan_data['hayvan'] = hayvan
            
            # Bitiş tarihi otomatik ayarla (60 gün sonra)
            if not ilan_data.get('bitis_tarihi'):
                ilan_data['bitis_tarihi'] = timezone.now() + timedelta(days=60)
            
            # İlanı oluştur
            ilan = Ilan.objects.create(**ilan_data)
            
            return ilan
            
        except Hayvan.DoesNotExist:
            raise PlatformBaseException(
                message=_("Hayvan bulunamadı"),
                code="HAYVAN_BULUNAMADI"
            )
        except Exception as e:
            raise PlatformBaseException(
                message=_("İlan oluşturulamadı: {error}").format(error=str(e)),
                code="ILAN_OLUSTURMA_HATASI"
            )
    
    @staticmethod
    def ilan_ara(arama_terimi: str, filtreler: Dict = None) -> List[Ilan]:
        """
        İlan arama
        """
        from django.db.models import Q
        
        queryset = Ilan.objects.filter(durum='aktif')
        
        # Arama terimi
        if arama_terimi:
            queryset = queryset.filter(
                Q(baslik__icontains=arama_terimi) |
                Q(aciklama__icontains=arama_terimi) |
                Q(hayvan__ad__icontains=arama_terimi)
            )
        
        # Filtreler uygula
        if filtreler:
            if filtreler.get('ilan_turu'):
                queryset = queryset.filter(ilan_turu=filtreler['ilan_turu'])
            
            if filtreler.get('il'):
                queryset = queryset.filter(il__iexact=filtreler['il'])
            
            if filtreler.get('acil') is not None:
                queryset = queryset.filter(acil=filtreler['acil'])
            
            if filtreler.get('ucretsiz') is not None:
                queryset = queryset.filter(ucretsiz=filtreler['ucretsiz'])
            
            # Fiyat aralığı
            if filtreler.get('min_fiyat'):
                queryset = queryset.filter(fiyat__gte=filtreler['min_fiyat'])
            
            if filtreler.get('max_fiyat'):
                queryset = queryset.filter(fiyat__lte=filtreler['max_fiyat'])
        
        return queryset.order_by('-acil', '-yayinlanma_tarihi')
    
    @staticmethod
    @transaction.atomic
    def basvuru_yap(ilan_id: int, basvuru_data: Dict) -> IlanBasvuru:
        """
        İlana başvuru yap
        """
        try:
            ilan = Ilan.objects.get(id=ilan_id, durum='aktif')
            
            # Aynı kişi daha önce başvuru yapmış mı?
            mevcut_basvuru = IlanBasvuru.objects.filter(
                ilan=ilan,
                basvuran_email=basvuru_data['basvuran_email']
            ).first()
            
            if mevcut_basvuru:
                raise PlatformBaseException(
                    message=_("Bu ilana daha önce başvuru yaptınız"),
                    code="ZATEN_BASVURU_VAR"
                )
            
            # Başvuru oluştur
            basvuru_data['ilan'] = ilan
            basvuru = IlanBasvuru.objects.create(**basvuru_data)
            
            return basvuru
            
        except Ilan.DoesNotExist:
            raise PlatformBaseException(
                message=_("İlan bulunamadı veya aktif değil"),
                code="ILAN_BULUNAMADI"
            )
    
    @staticmethod
    def acil_ilanlar(limit: int = 10) -> List[Ilan]:
        """
        Acil ilanları getir
        """
        return Ilan.objects.filter(
            durum='aktif',
            acil=True
        ).order_by('-yayinlanma_tarihi')[:limit]
    
    @staticmethod
    def son_ilanlar(limit: int = 10) -> List[Ilan]:
        """
        Son ilanları getir
        """
        return Ilan.objects.filter(
            durum='aktif'
        ).order_by('-yayinlanma_tarihi')[:limit]
    
    @staticmethod
    def il_istatistikleri() -> Dict:
        """
        İl bazında ilan istatistikleri
        """
        from django.db.models import Count
        
        return dict(
            Ilan.objects.filter(durum='aktif')
            .values('il')
            .annotate(count=Count('id'))
            .values_list('il', 'count')
        )
    
    @staticmethod
    def ilan_turu_istatistikleri() -> Dict:
        """
        İlan türü istatistikleri
        """
        from django.db.models import Count
        
        return dict(
            Ilan.objects.filter(durum='aktif')
            .values('ilan_turu')
            .annotate(count=Count('id'))
            .values_list('ilan_turu', 'count')
        )
    
    @staticmethod
    @transaction.atomic
    def ilan_durumu_guncelle(ilan_id: int, yeni_durum: str) -> Ilan:
        """
        İlan durumunu güncelle
        """
        try:
            ilan = Ilan.objects.get(id=ilan_id)
            ilan.durum = yeni_durum
            ilan.save(update_fields=['durum'])
            
            return ilan
            
        except Ilan.DoesNotExist:
            raise PlatformBaseException(
                message=_("İlan bulunamadı"),
                code="ILAN_BULUNAMADI"
            )
    
    @staticmethod
    def basvuru_durumu_guncelle(basvuru_id: int, yeni_durum: str) -> IlanBasvuru:
        """
        Başvuru durumunu güncelle
        """
        try:
            basvuru = IlanBasvuru.objects.get(id=basvuru_id)
            basvuru.durum = yeni_durum
            basvuru.save(update_fields=['durum'])
            
            return basvuru
            
        except IlanBasvuru.DoesNotExist:
            raise PlatformBaseException(
                message=_("Başvuru bulunamadı"),
                code="BASVURU_BULUNAMADI"
            )
