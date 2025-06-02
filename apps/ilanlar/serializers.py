"""
📢 İlanlar Serializers
==============================================================================
İlan API'si için veri formatları
==============================================================================
"""

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Ilan, IlanBasvuru, IlanFotograf
from apps.hayvanlar.serializers import HayvanDetailSerializer, HayvanListSerializer


class IlanFotografSerializer(serializers.ModelSerializer):
    """İlan fotoğraf serializer"""
    
    class Meta:
        model = IlanFotograf
        fields = ['id', 'fotograf', 'aciklama', 'sira']


class IlanListSerializer(serializers.ModelSerializer):
    """İlan liste serializer - özet bilgiler"""
    
    ilan_turu_display = serializers.CharField(source='get_ilan_turu_display', read_only=True)
    durum_display = serializers.CharField(source='get_durum_display', read_only=True)
    hayvan_adi = serializers.CharField(source='hayvan.ad', read_only=True)
    kapak_fotografi = serializers.SerializerMethodField()
    
    class Meta:
        model = Ilan
        fields = [
            'id', 'baslik', 'ilan_turu', 'ilan_turu_display',
            'durum', 'durum_display', 'hayvan_adi', 'kapak_fotografi',
            'il', 'ilce', 'acil', 'ucretsiz', 'yayinlanma_tarihi'
        ]
    
    def get_kapak_fotografi(self, obj):
        if obj.fotograflar.exists():
            foto = obj.fotograflar.first()
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(foto.fotograf.url)
            return foto.fotograf.url
        return None


class IlanDetailSerializer(serializers.ModelSerializer):
    """İlan detay serializer - tüm bilgiler"""
    
    ilan_turu_display = serializers.CharField(source='get_ilan_turu_display', read_only=True)
    durum_display = serializers.CharField(source='get_durum_display', read_only=True)
    hayvan = HayvanDetailSerializer(read_only=True)
    fotograflar = IlanFotografSerializer(many=True, read_only=True)
    
    class Meta:
        model = Ilan
        fields = [
            'id', 'baslik', 'aciklama', 'ilan_turu', 'ilan_turu_display',
            'durum', 'durum_display', 'hayvan', 'fotograflar',
            'ilan_veren_adi', 'ilan_veren_telefon', 'ilan_veren_email',
            'il', 'ilce', 'adres_detay', 'acil', 'ucretsiz', 'fiyat',
            'goruntulenme_sayisi', 'yayinlanma_tarihi', 'bitis_tarihi',
            'created_at', 'updated_at'
        ]


class IlanCreateSerializer(serializers.ModelSerializer):
    """İlan oluşturma serializer"""
    
    class Meta:
        model = Ilan
        fields = [
            'baslik', 'aciklama', 'ilan_turu', 'hayvan',
            'ilan_veren_adi', 'ilan_veren_telefon', 'ilan_veren_email',
            'il', 'ilce', 'adres_detay', 'acil', 'ucretsiz', 'fiyat'
        ]
    
    def validate_baslik(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(_("İlan başlığı en az 10 karakter olmalıdır."))
        return value
    
    def validate(self, data):
        # Ücretli ilan ise fiyat zorunlu
        if not data.get('ucretsiz') and not data.get('fiyat'):
            raise serializers.ValidationError({
                'fiyat': _("Ücretli ilanlar için fiyat belirtilmelidir.")
            })
        return data


class IlanBasvuruSerializer(serializers.ModelSerializer):
    """İlan başvuru serializer"""
    
    class Meta:
        model = IlanBasvuru
        fields = [
            'id', 'ilan', 'basvuran_adi', 'basvuran_telefon',
            'basvuran_email', 'mesaj', 'durum', 'created_at'
        ]
        read_only_fields = ['id', 'durum', 'created_at']
    
    def validate_mesaj(self, value):
        if len(value) < 20:
            raise serializers.ValidationError(_("Mesaj en az 20 karakter olmalıdır."))
        return value
