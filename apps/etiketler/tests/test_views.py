"""
🏷️ Evcil Hayvan Platformu - Etiket Views Testleri
==============================================================================
Etiket API endpoint testleri
==============================================================================
"""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.etiketler.models import Etiket
from apps.kullanicilar.models import CustomUser


@pytest.fixture
def api_client():
    """API istekleri için client"""
    return APIClient()


@pytest.fixture
def kullanici():
    """Test kullanıcısı oluştur"""
    return CustomUser.objects.create_user(
        email="test@example.com",
        password="test1234",
        first_name="Test",
        last_name="User"
    )


@pytest.fixture
def etiketler():
    """Test etiketleri listesi"""
    return [
        Etiket.objects.create(ad="Sevimli", renk_kodu="#FF5733"),
        Etiket.objects.create(ad="Oyuncu", renk_kodu="#33FF57"),
        Etiket.objects.create(ad="Sakin", renk_kodu="#5733FF"),
        Etiket.objects.create(ad="Evcil", renk_kodu="#F5F5F5"),
        Etiket.objects.create(ad="Aşılı", renk_kodu="#00AABB"),
    ]


@pytest.mark.django_db
class TestEtiketViewSet:
    """Etiket API testleri"""
    
    def test_etiket_listesi(self, api_client, etiketler):
        """Etiketleri listeleme testi"""
        url = reverse('etiket-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= len(etiketler)
        
    def test_etiket_detay(self, api_client, etiketler):
        """Etiket detay görüntüleme testi"""
        etiket = etiketler[0]
        url = reverse('etiket-detail', kwargs={'pk': etiket.id})
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['ad'] == etiket.ad
        assert response.data['slug'] == etiket.slug
        assert response.data['renk_kodu'] == etiket.renk_kodu
        assert 'iliskili_etiketler' in response.data
    
    def test_etiket_olusturma_yetkisiz(self, api_client):
        """Yetkisiz kullanıcı etiket oluşturma testi"""
        url = reverse('etiket-list')
        data = {
            'ad': 'Yeni Etiket',
            'aciklama': 'Bu bir test etiketidir',
            'renk_kodu': '#AABBCC'
        }
        
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_etiket_olusturma_yetkili(self, api_client, kullanici):
        """Yetkili kullanıcı etiket oluşturma testi"""
        # Kullanıcı girişi
        api_client.force_authenticate(user=kullanici)
        
        url = reverse('etiket-list')
        data = {
            'ad': 'Yeni Etiket',
            'aciklama': 'Bu bir test etiketidir',
            'renk_kodu': '#AABBCC'
        }
        
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['ad'] == 'Yeni Etiket'
        assert 'slug' in response.data
        
    def test_populer_etiketler(self, api_client, etiketler):
        """Popüler etiketler endpoint testi"""
        url = reverse('etiket-populer')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        
    def test_harfe_gore_etiketler(self, api_client, etiketler):
        """Harfe göre etiketler endpoint testi"""
        # 'S' harfiyle başlayan etiketler (Sevimli, Sakin)
        url = reverse('etiket-harfe-gore') + '?harf=s'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['harf'] == 's'
        assert len(response.data['etiketler']) == 2
        
    def test_etiket_guncelleme(self, api_client, etiketler, kullanici):
        """Etiket güncelleme testi"""
        etiket = etiketler[0]
        api_client.force_authenticate(user=kullanici)
        
        url = reverse('etiket-detail', kwargs={'pk': etiket.id})
        data = {
            'ad': etiket.ad,
            'aciklama': 'Güncellenmiş açıklama',
            'renk_kodu': '#EEDDFF'
        }
        
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['aciklama'] == 'Güncellenmiş açıklama'
        assert response.data['renk_kodu'] == '#EEDDFF'