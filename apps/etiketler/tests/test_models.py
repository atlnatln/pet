"""
🏷️ Evcil Hayvan Platformu - Etiket Model Testleri
==============================================================================
Etiket modeli için unit testler
==============================================================================
"""

import pytest
from django.utils.text import slugify
from apps.etiketler.models import Etiket


@pytest.mark.django_db
class TestEtiketModel:
    """Etiket modeli için test sınıfı"""
    
    def test_etiket_olusturma(self):
        """Etiket oluşturma temel testi"""
        etiket = Etiket.objects.create(
            ad="Test Etiket",
            aciklama="Test açıklama",
            renk_kodu="#FF5733"
        )
        
        # Temel doğrulamalar
        assert etiket.id is not None
        assert etiket.ad == "Test Etiket"
        assert etiket.slug == "test-etiket"
        assert etiket.renk_kodu == "#FF5733"
        assert etiket.aktif is True
        
    def test_etiket_str_metodu(self):
        """Etiketin string temsilinin doğru çalıştığını kontrol et"""
        etiket = Etiket.objects.create(
            ad="Oyuncu",
            aciklama="Oyuncu hayvanlar için"
        )
        assert str(etiket) == "Oyuncu"
        
    def test_otomatik_slug_olusturma(self):
        """Slug otomatik oluşturma özelliğini test et"""
        ad = "Özel Karakterli Etiket 123!"
        etiket = Etiket.objects.create(ad=ad)
        assert etiket.slug == slugify(ad)
        
    def test_benzersiz_slug_olusturma(self):
        """Aynı ada sahip etiketler için benzersiz slug oluşturduğunu kontrol et"""
        # İlk etiketi oluştur
        etiket1 = Etiket.objects.create(ad="Aynı Ad")
        assert etiket1.slug == "ayni-ad"
        
        # Aynı ada sahip ikinci etiketi oluştur
        etiket2 = Etiket.objects.create(ad="Aynı Ad")
        assert etiket2.slug != etiket1.slug
        assert etiket2.slug.startswith("ayni-ad-")
        
    def test_ayni_isimde_etiket_ekleme(self):
        """
        Aynı isme sahip bir etiket eklendiğinde, varolan etiketi aktifleştirip
        döndürmesini test et (büyük/küçük harf duyarsız)
        """
        # İlk etiketi oluştur ve pasif yap
        etiket1 = Etiket.objects.create(ad="Tatlı")
        etiket1.aktif = False
        etiket1.save()
        
        # Aynı ada sahip yeni etiket oluşturmayı dene (büyük harfle)
        etiket2 = Etiket(ad="TATLI")
        etiket2.save()
        
        # Veritabanındaki tüm etiket sayısını kontrol et
        assert Etiket.tum_etiketler.count() == 1
        
        # İlk etiketin aktif hale geldiğini doğrula
        etiket1.refresh_from_db()
        assert etiket1.aktif is True
        
    def test_renk_kodu_validasyonu(self):
        """Renk kodu validasyonunu test et"""
        from django.core.exceptions import ValidationError
        
        # Geçersiz renk kodu (# ile başlamıyor)
        etiket = Etiket(ad="Renk Test", renk_kodu="FF5733")
        
        with pytest.raises(ValidationError):
            etiket.full_clean()