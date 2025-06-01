"""
🐾 Evcil Hayvan Platformu - Hayvan Serializers
==============================================================================
Hayvanlar için API veri formatları
==============================================================================
"""

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Hayvan, HayvanFotograf, KopekIrk
from apps.kategoriler.models import Kategori
from apps.kategoriler.serializers import KategoriBasicSerializer


class KopekIrkSerializer(serializers.ModelSerializer):
    """Köpek ırkları serializer"""
    class Meta:
        model = KopekIrk
        fields = ['id', 'ad', 'aciklama', 'populer', 'yerli']


class HayvanFotografSerializer(serializers.ModelSerializer):
    """Hayvan fotoğrafları serializer"""
    class Meta:
        model = HayvanFotograf
        fields = ['id', 'fotograf', 'thumbnail', 'kapak_fotografi', 'sira']


class HayvanListSerializer(serializers.ModelSerializer):
    """Hayvan liste serializer - özet bilgiler"""
    
    tur_adi = serializers.CharField(source='get_tur_display', read_only=True)
    irk_adi = serializers.SerializerMethodField()
    kapak_fotografi_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Hayvan
        fields = [
            'id', 'ad', 'slug', 'tur', 'tur_adi', 
            'irk_adi', 'il', 'ilce', 'cinsiyet', 'yas',
            'kapak_fotografi_url', 'created_at', 'sahiplenildi'
        ]
    
    def get_irk_adi(self, obj):
        if obj.irk:
            return obj.irk.ad
        return None
    
    def get_kapak_fotografi_url(self, obj):
        if obj.kapak_fotografi:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.kapak_fotografi.fotograf.url)
            return obj.kapak_fotografi.fotograf.url
        return None


class HayvanDetailSerializer(serializers.ModelSerializer):
    """Hayvan detay serializer - tüm bilgiler"""
    
    tur_adi = serializers.CharField(source='get_tur_display', read_only=True)
    cinsiyet_adi = serializers.CharField(source='get_cinsiyet_display', read_only=True)
    yas_adi = serializers.CharField(source='get_yas_display', read_only=True)
    boyut_adi = serializers.CharField(source='get_boyut_display', read_only=True)
    kategori = KategoriBasicSerializer(read_only=True)
    irk = KopekIrkSerializer(read_only=True)
    fotograflar = HayvanFotografSerializer(many=True, read_only=True)
    
    class Meta:
        model = Hayvan
        fields = [
            'id', 'ad', 'slug', 'tur', 'tur_adi', 'kategori',
            'irk', 'yas', 'yas_adi', 'cinsiyet', 'cinsiyet_adi',
            'boyut', 'boyut_adi', 'renk', 'kisirlastirilmis',
            'asilar_tamam', 'mikrocipli', 'karakter_ozellikleri',
            'aciklama', 'il', 'ilce', 'sahiplenildi', 'aktif',
            'created_at', 'updated_at', 'fotograflar'
        ]


class HayvanCreateUpdateSerializer(serializers.ModelSerializer):
    """Hayvan oluşturma/güncelleme serializer"""
    
    class Meta:
        model = Hayvan
        fields = [
            'ad', 'tur', 'kategori', 'irk', 'yas', 'cinsiyet',
            'boyut', 'renk', 'kisirlastirilmis', 'asilar_tamam',
            'mikrocipli', 'karakter_ozellikleri', 'aciklama',
            'il', 'ilce', 'aktif'
        ]
    
    def validate_ad(self, value):
        if len(value) < 2:
            raise serializers.ValidationError(_("Hayvan adı en az 2 karakter olmalıdır."))
        return value
    
    def validate(self, data):
        # Tür köpek ise ırk kontrolü
        if data.get('tur') == 'kopek' and not data.get('irk'):
            raise serializers.ValidationError({
                'irk': _("Köpek türü için ırk bilgisi gerekli.")
            })
        return data


class HayvanFotografEkleSerializer(serializers.ModelSerializer):
    """Hayvan fotoğrafı ekleme serializer"""
    
    class Meta:
        model = HayvanFotograf
        fields = ['fotograf', 'kapak_fotografi', 'sira']


# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Bu serializer'lar, kategori verilerinin API'de tutarlı ve güvenli
# şekilde sunulmasını sağlar. Her endpoint'in kendine özel serializer'ı var.
# 🐾 Her API çağrısı, temiz ve anlaşılır veri döner!