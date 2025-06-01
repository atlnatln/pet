"""
🐾 Evcil Hayvan Platformu - Hayvan Servisleri
==============================================================================
Hayvanlarla ilgili iş mantığı ve servisler
==============================================================================
"""

from typing import List, Dict, Optional
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from apps.ortak.exceptions import PlatformBaseException
from .models import Hayvan, HayvanFotograf, KopekIrk


class HayvanService:
    """
    Hayvanlarla ilgili iş mantığı servisleri
    """
    
    @staticmethod
    @transaction.atomic
    def hayvan_olustur(data: Dict, user=None) -> Hayvan:
        """
        Yeni hayvan kayıt servisi
        
        Args:
            data: Hayvan verileri
            user: Kaydı oluşturan kullanıcı
        
        Returns:
            Hayvan: Oluşturulan hayvan
        """
        try:
            # Slug otomatik oluşacak
            hayvan = Hayvan.objects.create(**data)
            
            # TODO: Kullanıcı ile ilişkilendirme (kullanıcı modeli hazır olduğunda)
            # if user:
            #     hayvan.olusturan = user
            #     hayvan.save(update_fields=['olusturan'])
            
            return hayvan
            
        except ValidationError as e:
            raise PlatformBaseException(
                message=_("Hayvan oluşturulamadı: {error}").format(error=str(e)),
                code="HAYVAN_OLUSTURMA_HATASI"
            )
    
    @staticmethod
    def hayvan_listele(filtreler: Dict = None) -> List[Hayvan]:
        """
        Filtrelere göre hayvanları listele
        
        Args:
            filtreler: Filtre parametreleri
        
        Returns:
            List[Hayvan]: Hayvan listesi
        """
        queryset = Hayvan.objects.filter(aktif=True)
        
        if not filtreler:
            return queryset.order_by('-created_at')
        
        # Temel filtreler
        temel_filtreler = {
            'tur', 'kategori', 'cinsiyet', 'yas', 'boyut',
            'il', 'sahiplenildi'
        }
        
        for filtre in temel_filtreler:
            if filtre in filtreler and filtreler[filtre]:
                queryset = queryset.filter(**{filtre: filtreler[filtre]})
        
        # Özel filtreler
        if 'irk_id' in filtreler and filtreler['irk_id']:
            queryset = queryset.filter(irk_id=filtreler['irk_id'])
            
        if 'karakter' in filtreler and filtreler['karakter']:
            for ozellik in filtreler['karakter'].split(','):
                queryset = queryset.filter(karakter_ozellikleri__contains=[ozellik.strip()])
        
        # Boolean filtreler
        bool_filtreler = ['kisirlastirilmis', 'asilar_tamam', 'mikrocipli']
        for filtre in bool_filtreler:
            if filtre in filtreler and filtreler[filtre] is not None:
                queryset = queryset.filter(**{filtre: filtreler[filtre]})
        
        # Arama
        if 'search' in filtreler and filtreler['search']:
            from django.db.models import Q
            term = filtreler['search']
            queryset = queryset.filter(
                Q(ad__icontains=term) | Q(aciklama__icontains=term) |
                Q(irk__ad__icontains=term) | Q(kategori__ad__icontains=term)
            )
        
        # Sıralama
        sort_by = filtreler.get('sort', '-created_at')
        return queryset.order_by(sort_by)
    
    @staticmethod
    @transaction.atomic
    def hayvan_guncelle(hayvan_id: int, data: Dict) -> Hayvan:
        """
        Hayvan güncelleme servisi
        
        Args:
            hayvan_id: Güncellenecek hayvanın ID'si
            data: Güncellenecek veriler
        
        Returns:
            Hayvan: Güncellenen hayvan
        """
        try:
            hayvan = Hayvan.objects.get(id=hayvan_id)
            
            # Verileri güncelle
            for field, value in data.items():
                setattr(hayvan, field, value)
            
            hayvan.full_clean()
            hayvan.save()
            
            return hayvan
            
        except Hayvan.DoesNotExist:
            raise PlatformBaseException(
                message=_("Güncellenecek hayvan bulunamadı"),
                code="HAYVAN_BULUNAMADI"
            )
        except ValidationError as e:
            raise PlatformBaseException(
                message=_("Hayvan güncellenemedi: {error}").format(error=str(e)),
                code="HAYVAN_GUNCELLEME_HATASI"
            )
    
    @staticmethod
    @transaction.atomic
    def fotograf_ekle(hayvan_id: int, fotograf, kapak_fotografi: bool = False) -> HayvanFotograf:
        """
        Hayvana fotoğraf ekleme servisi
        
        Args:
            hayvan_id: Hayvan ID'si
            fotograf: Fotoğraf dosyası
            kapak_fotografi: Kapak fotoğrafı mı?
        
        Returns:
            HayvanFotograf: Eklenen fotoğraf
        """
        try:
            hayvan = Hayvan.objects.get(id=hayvan_id)
            
            # Bu fotoğraf kapak olacaksa mevcut kapakları kaldır
            if kapak_fotografi:
                HayvanFotograf.objects.filter(hayvan=hayvan, kapak_fotografi=True).update(
                    kapak_fotografi=False
                )
            
            # Fotoğraf ekle
            foto = HayvanFotograf.objects.create(
                hayvan=hayvan,
                fotograf=fotograf,
                kapak_fotografi=kapak_fotografi
            )
            
            return foto
            
        except Hayvan.DoesNotExist:
            raise PlatformBaseException(
                message=_("Fotoğraf eklenecek hayvan bulunamadı"),
                code="HAYVAN_BULUNAMADI"
            )
    
    @staticmethod
    def irklari_getir() -> List[Dict]:
        """
        Köpek ırklarını getir
        
        Returns:
            List[Dict]: Irk listesi
        """
        return list(KopekIrk.objects.filter(
            aktif=True
        ).values('id', 'ad', 'populer', 'yerli'))
    
    @staticmethod
    def populer_irklari_getir(limit: int = 10) -> List[Dict]:
        """
        Popüler köpek ırklarını getir
        
        Args:
            limit: Sonuç sayısı
        
        Returns:
            List[Dict]: Popüler ırk listesi
        """
        return list(KopekIrk.objects.filter(
            aktif=True, populer=True
        ).values('id', 'ad')[:limit])
    
    @staticmethod
    def yerli_irklari_getir() -> List[Dict]:
        """
        Yerli köpek ırklarını getir
        
        Returns:
            List[Dict]: Yerli ırk listesi
        """
        return list(KopekIrk.objects.filter(
            aktif=True, yerli=True
        ).values('id', 'ad'))
