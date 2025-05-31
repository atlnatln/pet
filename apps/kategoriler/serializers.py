"""
🐾 Kategoriler API Serializers
==============================================================================
Kategori verilerinin API formatında sunumu
==============================================================================
"""

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Kategori, KategoriOzellik


class KategoriOzellikSerializer(serializers.ModelSerializer):
    """
    Kategori özellik serializer
    """
    
    class Meta:
        model = KategoriOzellik
        fields = [
            'id', 'ad', 'alan_tipi', 'secenekler', 
            'zorunlu', 'sira'
        ]
        read_only_fields = ['id']


class KategoriBasicSerializer(serializers.ModelSerializer):
    """
    Temel kategori bilgileri (liste görünümü için)
    """
    
    pet_type_display = serializers.CharField(source='get_pet_type_display', read_only=True)
    tam_ad = serializers.CharField(read_only=True)
    seviye = serializers.IntegerField(read_only=True)
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    
    class Meta:
        model = Kategori
        fields = [
            'id', 'ad', 'slug', 'aciklama', 'pet_type', 
            'pet_type_display', 'ikon_adi', 'renk_kodu',
            'kullanim_sayisi', 'tam_ad', 'seviye', 'url'
        ]
        read_only_fields = ['id', 'slug', 'kullanim_sayisi']


class KategoriDetailSerializer(serializers.ModelSerializer):
    """
    Detaylı kategori bilgileri
    """
    
    pet_type_display = serializers.CharField(source='get_pet_type_display', read_only=True)
    tam_ad = serializers.CharField(read_only=True)
    seviye = serializers.IntegerField(read_only=True)
    alt_kategori_sayisi = serializers.IntegerField(read_only=True)
    toplam_hayvan_sayisi = serializers.IntegerField(read_only=True)
    breadcrumbs = serializers.JSONField(source='get_breadcrumbs', read_only=True)
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    
    # İlişkili veriler
    parent = KategoriBasicSerializer(read_only=True)
    alt_kategoriler = KategoriBasicSerializer(many=True, read_only=True)
    ozellikler = KategoriOzellikSerializer(many=True, read_only=True)
    
    class Meta:
        model = Kategori
        fields = [
            'id', 'ad', 'slug', 'aciklama', 'pet_type', 
            'pet_type_display', 'ikon_adi', 'renk_kodu',
            'kullanim_sayisi', 'tam_ad', 'seviye', 
            'alt_kategori_sayisi', 'toplam_hayvan_sayisi',
            'breadcrumbs', 'url', 'olusturulma_tarihi',
            'parent', 'alt_kategoriler', 'ozellikler'
        ]
        read_only_fields = [
            'id', 'slug', 'kullanim_sayisi', 'olusturulma_tarihi'
        ]


class KategoriTreeSerializer(serializers.ModelSerializer):
    """
    Kategori ağaç yapısı serializer
    """
    
    pet_type_display = serializers.CharField(source='get_pet_type_display', read_only=True)
    children = serializers.SerializerMethodField()
    hayvan_sayisi = serializers.IntegerField(source='kullanim_sayisi', read_only=True)
    
    class Meta:
        model = Kategori
        fields = [
            'id', 'ad', 'slug', 'aciklama', 'pet_type',
            'pet_type_display', 'ikon_adi', 'renk_kodu',
            'hayvan_sayisi', 'children'
        ]
    
    def get_children(self, obj):
        """Alt kategorileri getir"""
        if hasattr(obj, 'prefetched_children'):
            # Prefetch edilmiş alt kategoriler varsa kullan
            children = obj.prefetched_children
        else:
            # Yoksa sorgula
            children = obj.alt_kategoriler.filter(aktif=True).order_by('sira', 'ad')
        
        return KategoriTreeSerializer(children, many=True, context=self.context).data


class KategoriStatsSerializer(serializers.Serializer):
    """
    Kategori istatistik serializer
    """
    
    toplam_kategori = serializers.IntegerField()
    ana_kategori_sayisi = serializers.IntegerField()
    alt_kategori_sayisi = serializers.IntegerField()
    pet_type_dagilimi = serializers.DictField()
    populer_kategoriler = KategoriBasicSerializer(many=True)
    
    class Meta:
        fields = [
            'toplam_kategori', 'ana_kategori_sayisi', 
            'alt_kategori_sayisi', 'pet_type_dagilimi',
            'populer_kategoriler'
        ]


class KategoriCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Kategori oluşturma/güncelleme serializer
    """
    
    class Meta:
        model = Kategori
        fields = [
            'ad', 'aciklama', 'parent', 'pet_type',
            'ikon_adi', 'renk_kodu', 'aktif', 'sira'
        ]
    
    def validate_ad(self, value):
        """Kategori adı validasyonu"""
        if len(value) < 2:
            raise serializers.ValidationError(
                _("Kategori adı en az 2 karakter olmalıdır.")
            )
        
        # Aynı parent altında aynı isimde kategori kontrolü
        parent = self.initial_data.get('parent')
        existing = Kategori.objects.filter(
            ad__iexact=value, 
            parent=parent
        )
        
        if self.instance:
            existing = existing.exclude(pk=self.instance.pk)
        
        if existing.exists():
            if parent:
                raise serializers.ValidationError(
                    _("Bu ana kategori altında aynı isimde bir kategori zaten var.")
                )
            else:
                raise serializers.ValidationError(
                    _("Bu isimde bir ana kategori zaten var.")
                )
        
        return value
    
    def validate_parent(self, value):
        """Parent kategori validasyonu"""
        if value and self.instance:
            # Kendi kendini parent yapamaz
            if value.pk == self.instance.pk:
                raise serializers.ValidationError(
                    _("Kategori kendi kendisinin ana kategorisi olamaz.")
                )
            
            # Circular reference kontrolü
            current = value
            while current.parent:
                if current.parent.pk == self.instance.pk:
                    raise serializers.ValidationError(
                        _("Bu seçim döngüsel bir referans oluşturacaktır.")
                    )
                current = current.parent
        
        return value
    
    def validate_renk_kodu(self, value):
        """Renk kodu validasyonu"""
        import re
        if not re.match(r'^#[0-9A-Fa-f]{6}$', value):
            raise serializers.ValidationError(
                _("Geçerli bir HEX renk kodu giriniz (örn: #ff0000).")
            )
        return value


class KategoriFilterSerializer(serializers.Serializer):
    """
    Kategori filtreleme serializer
    """
    
    pet_type = serializers.ChoiceField(
        choices=[('', 'Tümü')] + list(Kategori._meta.get_field('pet_type').choices),
        required=False,
        allow_blank=True
    )
    
    parent = serializers.IntegerField(required=False, allow_null=True)
    
    aktif = serializers.BooleanField(required=False, default=True)
    
    arama = serializers.CharField(
        required=False, 
        allow_blank=True,
        max_length=100,
        help_text=_("Kategori adı veya açıklamada arama")
    )
    
    def validate_arama(self, value):
        """Arama terimi validasyonu"""
        if value and len(value) < 2:
            raise serializers.ValidationError(
                _("Arama terimi en az 2 karakter olmalıdır.")
            )
        return value

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Bu serializer'lar, kategori verilerinin API'de tutarlı ve güvenli
# şekilde sunulmasını sağlar. Her endpoint'in kendine özel serializer'ı var.
# 🐾 Her API çağrısı, temiz ve anlaşılır veri döner!
