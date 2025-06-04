"""
🏷️ Evcil Hayvan Platformu - Etiket Servisleri Testleri
==============================================================================
Etiket servisleri için test sınıfları
==============================================================================
"""

import pytest
from django.db import transaction

from apps.etiketler.models import Etiket
from apps.etiketler.servisler import EtiketService
from apps.hayvanlar.models import Hayvan
from apps.kategoriler.models import Kategori
from apps.kullanicilar.models import CustomUser


@pytest.fixture
def test_user():
    """Test kullanıcısı"""
    return CustomUser.objects.create_user(
        email="test@example.com",
        password="test1234",
        first_name="Test",
        last_name="User"
    )

@pytest.fixture
def kategori():
    """Test kategorisi"""
    return Kategori.objects.create(
        ad="Test Kategori",
        aciklama="Test kategori açıklaması"
    )

@pytest.fixture
def hayvan(test_user, kategori):
    """Test hayvanı"""
    return Hayvan.objects.create(
        ad="Test Hayvan",
        tur="kedi",
        kategori=kategori,
        cinsiyet="disi",
        sorumlu=test_user,
        aciklama="Test hayvanı açıklaması"
    )


@pytest.mark.django_db
class TestEtiketService:
    """Etiket servisleri için test sınıfı"""
    
    def test_etiket_olustur_veya_getir(self):
        """Etiket oluştur veya getir metodu testi"""
        # Yeni etiket oluşturma
        etiket1 = EtiketService.etiket_olustur_veya_getir("Yeni Etiket")
        assert etiket1.id is not None
        assert etiket1.ad == "Yeni Etiket"
        assert etiket1.aktif is True
        
        # Aynı etiketi tekrar istemek
        etiket2 = EtiketService.etiket_olustur_veya_getir("Yeni Etiket")
        assert etiket1.id == etiket2.id  # Aynı etiketi döndürmeli
        
        # Pasif etiketi aktifleştirmek
        etiket1.aktif = False
        etiket1.save()
        
        etiket3 = EtiketService.etiket_olustur_veya_getir("Yeni Etiket")
        assert etiket3.aktif is True  # Etiket aktifleştirilmiş olmalı
        assert etiket1.id == etiket3.id  # Aynı etiketi döndürmeli
        
        # Büyük/küçük harf farklı fakat aynı etiket
        etiket4 = EtiketService.etiket_olustur_veya_getir("YENİ ETİKET")
        assert etiket1.id == etiket4.id  # Aynı etiketi döndürmeli
        
    def test_etiketleri_guncelle(self, hayvan):
        """Etiketleri güncelle metodu testi"""
        # İlk etiketler ekleniyor
        ilk_etiketler = ["Sevimli", "Oyuncu", "Aşılı"]
        
        with transaction.atomic():
            sonuc1 = EtiketService.etiketleri_guncelle(hayvan, ilk_etiketler)
            
        # Sonuçları doğrula
        assert len(sonuc1['eklenen']) == 3
        assert len(sonuc1['kaldirilan']) == 0
        assert len(sonuc1['degismedi']) == 0
        assert hayvan.etiketler.count() == 3
        
        # Etiketleri değiştir (bir ekleme, bir çıkarma)
        yeni_etiketler = ["Sevimli", "Oyuncu", "Sakin"]  # Aşılı çıktı, Sakin eklendi
        
        with transaction.atomic():
            sonuc2 = EtiketService.etiketleri_guncelle(hayvan, yeni_etiketler)
            
        # Sonuçları doğrula
        assert len(sonuc2['eklenen']) == 1
        assert "Sakin" in sonuc2['eklenen']
        assert len(sonuc2['kaldirilan']) == 1
        assert "Aşılı" in sonuc2['kaldirilan']
        assert len(sonuc2['degismedi']) == 2
        assert hayvan.etiketler.count() == 3
        
        # Tüm etiketleri kaldır
        with transaction.atomic():
            sonuc3 = EtiketService.etiketleri_guncelle(hayvan, [])
            
        # Sonuçları doğrula
        assert len(sonuc3['eklenen']) == 0
        assert len(sonuc3['kaldirilan']) == 3
        assert hayvan.etiketler.count() == 0
        
    def test_benzer_etiketler_onerisi(self):
        """Benzer etiketler önerisi metodu testi"""
        # Öneri için bazı etiketler oluşturalım
        Etiket.objects.create(ad="Sevimli")
        Etiket.objects.create(ad="Oyuncu")
        Etiket.objects.create(ad="Sakin")
        Etiket.objects.create(ad="Aşılı")
        Etiket.objects.create(ad="Evcil")
        
        # Öneri için metin
        metin = """
        Bu sevimli ve oyuncu kedi çok sakin bir yapıya sahip.
        Tüm aşıları tamamlanmış ve ev ortamında yaşamaya alışkın.
        """
        
        oneriler = EtiketService.benzer_etiketler_onerisi(metin, limit=3)
        
        # En az bir öneri olmalı
        assert len(oneriler) > 0
        # Metnin içerisinde geçen etiketlerden en az biri önerilerde olmalı
        assert any(oneri.lower() in ["sevimli", "oyuncu", "sakin", "aşılı", "evcil"] for oneri in oneriler)