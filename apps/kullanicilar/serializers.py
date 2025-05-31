"""
🐾 Kullanıcılar API Serializers
==============================================================================
Kullanıcı verilerinin API formatında sunumu
==============================================================================
"""

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import CustomUser, KullaniciProfil
from .validators import validate_strong_user_password, validate_turkish_phone


class KullaniciProfilSerializer(serializers.ModelSerializer):
    """
    Kullanıcı profil detay serializer
    """
    
    class Meta:
        model = KullaniciProfil
        fields = [
            'instagram_hesabi', 'facebook_hesabi', 'hayvan_deneyimi_yil',
            'daha_once_sahiplendin_mi', 'veteriner_referansi', 'ev_tipi',
            'bahce_var_mi', 'diger_hayvanlar', 'referans_kisi_1', 
            'referans_kisi_2', 'kimlik_dogrulandi_mi'
        ]
        read_only_fields = ['kimlik_dogrulandi_mi']


class UserBasicSerializer(serializers.ModelSerializer):
    """
    Temel kullanıcı bilgileri (liste görünümü için)
    """
    
    tam_ad = serializers.CharField(read_only=True)
    rol_display = serializers.CharField(source='get_rol_display', read_only=True)
    durum_display = serializers.CharField(source='get_durum_display', read_only=True)
    initials = serializers.CharField(source='get_initials', read_only=True)
    profil_tamamlama_yuzdesi = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'first_name', 'last_name', 'tam_ad',
            'sehir', 'rol', 'rol_display', 'durum', 'durum_display',
            'profil_resmi', 'initials', 'profil_tamamlama_yuzdesi',
            'email_dogrulanmis', 'uyelik_tarihi'
        ]
        read_only_fields = [
            'id', 'email_dogrulanmis', 'uyelik_tarihi'
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Detaylı kullanıcı bilgileri
    """
    
    tam_ad = serializers.CharField(read_only=True)
    rol_display = serializers.CharField(source='get_rol_display', read_only=True)
    durum_display = serializers.CharField(source='get_durum_display', read_only=True)
    profil_tamamlanmis_mi = serializers.BooleanField(read_only=True)
    profil_tamamlama_yuzdesi = serializers.IntegerField(read_only=True)
    aktif_mi = serializers.BooleanField(read_only=True)
    
    # İlişkili veriler
    profil_detay = KullaniciProfilSerializer(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'first_name', 'last_name', 'tam_ad',
            'telefon', 'sehir', 'biyografi', 'profil_resmi',
            'rol', 'rol_display', 'durum', 'durum_display',
            'sahiplendiren_mi', 'sahiplenmek_istiyor_mu',
            'email_bildirimleri', 'push_bildirimleri',
            'email_dogrulanmis', 'profil_tamamlanmis_mi',
            'profil_tamamlama_yuzdesi', 'aktif_mi',
            'uyelik_tarihi', 'son_giris_tarihi', 'giris_sayisi',
            'profil_detay'
        ]
        read_only_fields = [
            'id', 'email', 'email_dogrulanmis', 'uyelik_tarihi',
            'son_giris_tarihi', 'giris_sayisi'
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Kullanıcı kayıt serializer
    """
    
    password = serializers.CharField(
        write_only=True,
        validators=[validate_strong_user_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'telefon', 'sehir',
            'biyografi', 'sahiplendiren_mi', 'sahiplenmek_istiyor_mu'
        ]
    
    def validate_email(self, value):
        """E-posta validasyonu"""
        if CustomUser.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                _("Bu e-posta adresi zaten kullanılıyor.")
            )
        return value.lower()
    
    def validate_telefon(self, value):
        """Telefon validasyonu"""
        if value:
            validate_turkish_phone(value)
        return value
    
    def validate(self, attrs):
        """Çapraz alan validasyonu"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': _("Şifreler eşleşmiyor.")
            })
        
        # En az bir rol seçilmeli
        if not attrs.get('sahiplendiren_mi') and not attrs.get('sahiplenmek_istiyor_mu'):
            raise serializers.ValidationError(
                _("En az bir rol seçmelisiniz (sahiplendiren veya sahiplenmek isteyen).")
            )
        
        return attrs
    
    def create(self, validated_data):
        """Kullanıcı oluştur"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = CustomUser.objects.create_user(
            password=password,
            **validated_data
        )
        
        # Profil detayı oluştur
        KullaniciProfil.objects.create(kullanici=user)
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Kullanıcı giriş serializer
    """
    
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})
    
    def validate(self, attrs):
        """Giriş bilgileri validasyonu"""
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            # E-posta küçük harfe çevir
            email = email.lower()
            
            # Kullanıcıyı doğrula
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError(
                    _("E-posta veya şifre hatalı.")
                )
            
            if not user.is_active:
                raise serializers.ValidationError(
                    _("Bu hesap devre dışı bırakılmış.")
                )
            
            if user.durum != 'active':
                raise serializers.ValidationError(
                    _("Hesabınız aktif değil. Lütfen destek ile iletişime geçin.")
                )
            
            attrs['user'] = user
            return attrs
        
        raise serializers.ValidationError(
            _("E-posta ve şifre gereklidir.")
        )


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Kullanıcı profil güncelleme serializer
    """
    
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'telefon', 'sehir',
            'biyografi', 'profil_resmi', 'sahiplendiren_mi',
            'sahiplenmek_istiyor_mu', 'email_bildirimleri',
            'push_bildirimleri'
        ]
    
    def validate_telefon(self, value):
        """Telefon validasyonu"""
        if value:
            validate_turkish_phone(value)
        return value
    
    def validate(self, attrs):
        """En az bir rol kontrolü"""
        # Mevcut değerleri al
        instance = self.instance
        sahiplendiren = attrs.get('sahiplendiren_mi', instance.sahiplendiren_mi)
        sahiplenmek = attrs.get('sahiplenmek_istiyor_mu', instance.sahiplenmek_istiyor_mu)
        
        if not sahiplendiren and not sahiplenmek:
            raise serializers.ValidationError(
                _("En az bir rol seçmelisiniz.")
            )
        
        return attrs


class PasswordChangeSerializer(serializers.Serializer):
    """
    Şifre değiştirme serializer
    """
    
    old_password = serializers.CharField(style={'input_type': 'password'})
    new_password = serializers.CharField(
        validators=[validate_strong_user_password],
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(style={'input_type': 'password'})
    
    def validate_old_password(self, value):
        """Eski şifre kontrolü"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                _("Mevcut şifre hatalı.")
            )
        return value
    
    def validate(self, attrs):
        """Yeni şifre kontrolü"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': _("Yeni şifreler eşleşmiyor.")
            })
        return attrs
    
    def save(self):
        """Şifreyi güncelle"""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Şifre sıfırlama talebi serializer
    """
    
    email = serializers.EmailField()
    
    def validate_email(self, value):
        """E-posta kontrolü"""
        try:
            user = CustomUser.objects.get(email__iexact=value.lower())
            if not user.is_active:
                raise serializers.ValidationError(
                    _("Bu hesap devre dışı bırakılmış.")
                )
        except CustomUser.DoesNotExist:
            # Güvenlik için gerçek hatayı verme
            pass
        
        return value.lower()


class EmailVerificationSerializer(serializers.Serializer):
    """
    E-posta doğrulama serializer
    """
    
    token = serializers.CharField()
    
    def validate_token(self, value):
        """Token kontrolü"""
        try:
            user = CustomUser.objects.get(
                email_dogrulama_token=value,
                email_dogrulanmis=False
            )
            self.context['user'] = user
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                _("Geçersiz veya süresi dolmuş token.")
            )
        
        return value


class UserStatsSerializer(serializers.Serializer):
    """
    Kullanıcı istatistik serializer
    """
    
    toplam_kullanici = serializers.IntegerField()
    aktif_kullanici = serializers.IntegerField()
    dogrulanmis_kullanici = serializers.IntegerField()
    sahiplendiren_sayisi = serializers.IntegerField()
    sahiplenmek_isteyen_sayisi = serializers.IntegerField()
    sehir_dagilimi = serializers.DictField()
    
    class Meta:
        fields = [
            'toplam_kullanici', 'aktif_kullanici', 'dogrulanmis_kullanici',
            'sahiplendiren_sayisi', 'sahiplenmek_isteyen_sayisi', 'sehir_dagilimi'
        ]

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Bu serializer'lar, kullanıcı sisteminin API'de güvenli ve tutarlı
# şekilde sunulmasını sağlar. Authentication, validation ve formatting bir arada.
# 🐾 Her API çağrısı, kullanıcı deneyimini önceleyerek tasarlandı!
