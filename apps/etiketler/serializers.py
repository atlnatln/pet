"""
🏷️ Evcil Hayvan Platformu - Etiketler Serializers
==============================================================================
Etiket modeli için API serializer sınıfları
==============================================================================
"""

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from .models import Etiket


class EtiketSerializer(serializers.ModelSerializer):
    """Etiket modeli için temel serializer"""
    kullanim_sayisi = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Etiket
        fields = [
            'id', 'ad', 'slug', 'aciklama', 'renk_kodu', 
            'ikon', 'kullanim_sayisi', 'olusturma_tarihi'
        ]
        read_only_fields = ['slug', 'kullanim_sayisi', 'olusturma_tarihi']


class EtiketCreateUpdateSerializer(serializers.ModelSerializer):
    """Etiket oluşturma/güncelleme için serializer"""
    
    class Meta:
        model = Etiket
        fields = ['ad', 'aciklama', 'renk_kodu', 'ikon']
        
    def validate_ad(self, value):
        """Etiket adı validasyonu"""
        if len(value) < 2:
            raise serializers.ValidationError(
                _("Etiket adı en az 2 karakter olmalıdır.")
            )
            
        # Özel karakterleri kontrol et
        if any(char in value for char in ['@', '#', '$', '%', '^', '&', '*']):
            raise serializers.ValidationError(
                _("Etiket adı özel karakter içeremez.")
            )
            
        return value
        
    def validate_renk_kodu(self, value):
        """Renk kodu validasyonu"""
        if value and not value.startswith('#'):
            value = f'#{value}'
            
        # Renk kodu formatını kontrol et (Hex kodu #RRGGBB formatında olmalı)
        if value and (len(value) != 7 or not all(c in '0123456789ABCDEFabcdef' for c in value[1:])):
            raise serializers.ValidationError(
                _("Geçerli bir HEX renk kodu giriniz (örn: #3B82F6)")
            )
            
        return value
    
    def create(self, validated_data):
        """Yeni etiket oluştur"""
        # Slug alanını otomatik oluşturmak için boş bırakıyoruz
        # Model içerisindeki save metodu slug oluşturacak
        return Etiket.objects.create(**validated_data)


class EtiketDetailSerializer(EtiketSerializer):
    """Etiket detay görünümü için genişletilmiş serializer"""
    iliskili_etiketler = serializers.SerializerMethodField()
    
    class Meta(EtiketSerializer.Meta):
        fields = EtiketSerializer.Meta.fields + ['iliskili_etiketler']
    
    def get_iliskili_etiketler(self, obj):
        """Etiket ile ilişkili diğer etiketleri döndürür"""
        iliskili = Etiket.objects.ile_ilgili(obj.ad, limit=5)
        return EtiketSerializer(iliskili, many=True).data