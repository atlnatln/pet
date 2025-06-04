"""
🏷️ Evcil Hayvan Platformu - Etiket Serializers Testleri
==============================================================================
Etiket serileştiricileri için testler
==============================================================================
"""

import pytest
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError

from apps.etiketler.models import Etiket
from apps.etiketler.serializers import (
    EtiketSerializer, 
    EtiketCreateUpdateSerializer, 
    EtiketDetailSerializer
)


@pytest.mark.django_db
class TestEtiketSerializers:
    """Etiket serileştiricileri için test sınıfı"""
    
    def test_etiket_serializer(self):
        """Temel etiket serileştiricisi testi"""
        etiket = Etiket.objects.create(
            ad="Test Etiket", 
            aciklama="Test açıklama",
            renk_kodu="#FF5733"
        )
        
        serializer = EtiketSerializer(etiket)
        data = serializer.data
        
        assert data['ad'] == "Test Etiket"
        assert data['slug'] == "test-etiket"
        assert data['aciklama'] == "Test açıklama"
        assert data['renk_kodu'] == "#FF5733"
        assert 'kullanim_sayisi' in data
        
    def test_etiket_create_serializer_valid(self):
        """Etiket oluşturma serileştirici validasyonu testi - geçerli veriler"""
        data = {
            'ad': 'Yeni Etiket',
            'aciklama': 'Yeni etiket açıklaması',
            'renk_kodu': '#123456',
            'ikon': 'paw'
        }
        
        serializer = EtiketCreateUpdateSerializer(data=data)
        assert serializer.is_valid()
        
        # # ifadesi olmadan renk kodu
        data['renk_kodu'] = '654321'
        serializer = EtiketCreateUpdateSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data['renk_kodu'] == '#654321'  # Otomatik # eklendi
        
    def test_etiket_create_serializer_invalid(self):
        """Etiket oluşturma serileştirici validasyonu testi - geçersiz veriler"""
        # Etiket adı çok kısa
        data = {
            'ad': 'A',
            'aciklama': 'Çok kısa ad',
            'renk_kodu': '#123456'
        }
        
        serializer = EtiketCreateUpdateSerializer(data=data)
        assert not serializer.is_valid()
        assert 'ad' in serializer.errors
        
        # Geçersiz renk kodu
        data = {
            'ad': 'Etiket',
            'aciklama': 'Açıklama',
            'renk_kodu': '#XYZ'  # Geçersiz hex
        }
        
        serializer = EtiketCreateUpdateSerializer(data=data)
        assert not serializer.is_valid()
        assert 'renk_kodu' in serializer.errors
        
        # Özel karakter içeren ad
        data = {
            'ad': 'Etiket@#$',
            'aciklama': 'Özel karakterli'
        }
        
        serializer = EtiketCreateUpdateSerializer(data=data)
        assert not serializer.is_valid()
        assert 'ad' in serializer.errors
        
    def test_etiket_detail_serializer(self):
        """Etiket detay serileştiricisi testi"""
        # Bazı etiketler oluşturalım
        etiket1 = Etiket.objects.create(ad="Sevimli")
        etiket2 = Etiket.objects.create(ad="Oyuncu")
        etiket3 = Etiket.objects.create(ad="Sakin")
        
        # Detay serileştirici
        serializer = EtiketDetailSerializer(etiket1)
        data = serializer.data
        
        assert data['ad'] == "Sevimli"
        assert 'iliskili_etiketler' in data