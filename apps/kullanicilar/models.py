"""
🐾 Kullanıcı Modelleri
==============================================================================
Platform kahramanlarının dijital kimlikleri - Her kullanıcının hikayesi
==============================================================================
"""

import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.utils import timezone
from apps.ortak.models import TimestampedModel
from apps.ortak.constants import UserRoles, UserStatus, TURKISH_CITIES
from apps.ortak.validators import validate_strong_password, validate_user_input_security
from apps.kullanicilar.managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    🐾 Custom User Model - Email tabanlı authentication
    ==============================================================================
    Platform için özelleştirilmiş kullanıcı modeli
    ==============================================================================
    """
    
    # Varsayılan username alanını kaldır
    username = None
    
    # Özel alanlar
    email = models.EmailField(
        _('E-posta'),
        unique=True,
        help_text=_('Giriş için kullanılacak e-posta adresi')
    )
    
    first_name = models.CharField(
        max_length=50,
        validators=[validate_user_input_security],
        verbose_name=_("Ad"),
        help_text=_("Gerçek adınız")
    )
    
    last_name = models.CharField(
        max_length=50,
        validators=[validate_user_input_security],
        verbose_name=_("Soyad"),
        help_text=_("Gerçek soyadınız")
    )
    
    # Profil bilgileri
    telefon = models.CharField(
        max_length=20,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^(\+90|0)?[5][0-9]{9}$',
                message=_("Geçerli bir Türkiye telefon numarası giriniz")
            )
        ],
        verbose_name=_("Telefon Numarası"),
        help_text=_("İletişim için telefon numaranız")
    )
    
    sehir = models.CharField(
        max_length=50,
        choices=TURKISH_CITIES,
        blank=True,
        verbose_name=_("Şehir"),
        help_text=_("Hangi şehirde yaşıyorsunuz?")
    )
    
    biyografi = models.TextField(
        max_length=500,
        blank=True,
        validators=[validate_user_input_security],
        verbose_name=_("Kısa Biyografi"),
        help_text=_("Kendinizi tanıtın - hayvan sevginizi anlatın (500 karakter)")
    )
    
    profil_resmi = models.ImageField(
        upload_to='profil_resimleri/%Y/%m/',
        blank=True,
        null=True,
        verbose_name=_("Profil Resmi"),
        help_text=_("Profil fotoğrafınız (5MB'a kadar)")
    )
    
    # Platform rolleri
    rol = models.CharField(
        max_length=20,
        choices=UserRoles.CHOICES,
        default=UserRoles.USER,
        verbose_name=_("Kullanıcı Rolü"),
        help_text=_("Platformdaki rolünüz")
    )
    
    durum = models.CharField(
        max_length=20,
        choices=UserStatus.CHOICES,
        default=UserStatus.ACTIVE,
        verbose_name=_("Hesap Durumu")
    )
    
    # Email doğrulama
    email_dogrulanmis = models.BooleanField(
        default=False,
        verbose_name=_("E-posta Doğrulandı"),
        help_text=_("E-posta adresi doğrulandı mı?")
    )
    
    email_dogrulama_token = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("E-posta Doğrulama Token")
    )
    
    email_dogrulama_tarihi = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("E-posta Doğrulama Tarihi")
    )
    
    # Kullanıcı tercihleri
    sahiplendiren_mi = models.BooleanField(
        default=False,
        verbose_name=_("Sahiplendiren"),
        help_text=_("Hayvan sahiplendirmek istiyorum")
    )
    
    sahiplenmek_istiyor_mu = models.BooleanField(
        default=True,
        verbose_name=_("Sahiplenmek İstiyor"),
        help_text=_("Hayvan sahiplenmek istiyorum")
    )
    
    # Bildirim tercihleri
    email_bildirimleri = models.BooleanField(
        default=True,
        verbose_name=_("E-posta Bildirimleri"),
        help_text=_("E-posta ile bildirim almak istiyorum")
    )
    
    push_bildirimleri = models.BooleanField(
        default=True,
        verbose_name=_("Push Bildirimleri"),
        help_text=_("Tarayıcı bildirimleri almak istiyorum")
    )
    
    # İstatistikler
    son_giris_tarihi = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Son Giriş Tarihi")
    )
    
    giris_sayisi = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Giriş Sayısı")
    )
    
    # Platform özel alanlar
    uyelik_tarihi = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Üyelik Tarihi")
    )
    
    guncelleme_tarihi = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Son Güncelleme")
    )
    
    # Özel manager
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        verbose_name = _("👤 Kullanıcı")
        verbose_name_plural = _("👤 Kullanıcılar") 
        ordering = ['-uyelik_tarihi']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['durum', 'email_dogrulanmis']),
            models.Index(fields=['sehir']),
            models.Index(fields=['rol']),
        ]
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def save(self, *args, **kwargs):
        # Email küçük harfe çevir
        if self.email:
            self.email = self.email.lower()
        
        # Username'i email ile senkronize et
        if not self.username or self.username != self.email:
            self.username = self.email
        
        super().save(*args, **kwargs)
    
    @property
    def tam_ad(self):
        """Tam ad döndür"""
        return self.get_full_name() or self.email.split('@')[0]
    
    @property
    def aktif_mi(self):
        """Kullanıcı aktif mi?"""
        return self.durum == UserStatus.ACTIVE and self.email_dogrulanmis
    
    @property
    def profil_tamamlanmis_mi(self):
        """Profil tamamlanmış mı?"""
        required_fields = [
            self.first_name, self.last_name, 
            self.telefon, self.sehir, self.biyografi
        ]
        return all(field for field in required_fields)
    
    @property
    def profil_tamamlama_yuzdesi(self):
        """Profil tamamlama yüzdesi"""
        fields = [
            self.first_name, self.last_name, self.telefon, 
            self.sehir, self.biyografi, self.profil_resmi
        ]
        completed = sum(1 for field in fields if field)
        return int((completed / len(fields)) * 100)
    
    def email_dogrula(self):
        """E-posta adresini doğrula"""
        self.email_dogrulanmis = True
        self.email_dogrulama_tarihi = timezone.now()
        self.email_dogrulama_token = ''
        self.save(update_fields=[
            'email_dogrulanmis', 'email_dogrulama_tarihi', 
            'email_dogrulama_token'
        ])
    
    def son_giris_guncelle(self):
        """Son giriş bilgilerini güncelle"""
        self.son_giris_tarihi = timezone.now()
        self.giris_sayisi += 1
        self.save(update_fields=['son_giris_tarihi', 'giris_sayisi'])
    
    def get_display_name(self):
        """Görüntülenecek isim"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        else:
            return self.email.split('@')[0]
    
    def get_initials(self):
        """İsim baş harfleri"""
        if self.first_name and self.last_name:
            return f"{self.first_name[0].upper()}{self.last_name[0].upper()}"
        elif self.first_name:
            return self.first_name[0].upper()
        else:
            return self.email[0].upper()


class KullaniciProfil(TimestampedModel):
    """
    Kullanıcı profil ek bilgileri
    """
    
    kullanici = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profil_detay',
        verbose_name=_("Kullanıcı")
    )
    
    # Sosyal medya
    instagram_hesabi = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Instagram Hesabı"),
        help_text=_("Instagram kullanıcı adınız")
    )
    
    facebook_hesabi = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Facebook Hesabı")
    )
    
    # Deneyim bilgileri
    hayvan_deneyimi_yil = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Hayvan Deneyimi (Yıl)"),
        help_text=_("Kaç yıldır hayvan bakıyorsunuz?")
    )
    
    daha_once_sahiplendin_mi = models.BooleanField(
        default=False,
        verbose_name=_("Daha Önce Sahiplendin mi?"),
        help_text=_("Daha önce hayvan sahiplendiniz mi?")
    )
    
    veteriner_referansi = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Veteriner Referansı"),
        help_text=_("Referans veteriner hekim bilgisi")
    )
    
    # Konut bilgileri
    ev_tipi = models.CharField(
        max_length=50,
        choices=[
            ('apartman', _('Apartman Dairesi')),
            ('mustakil', _('Müstakil Ev')),
            ('villa', _('Villa')),
            ('bahceli', _('Bahçeli Ev')),
            ('diger', _('Diğer')),
        ],
        blank=True,
        verbose_name=_("Ev Tipi")
    )
    
    bahce_var_mi = models.BooleanField(
        default=False,
        verbose_name=_("Bahçe Var mı?")
    )
    
    diger_hayvanlar = models.TextField(
        max_length=300,
        blank=True,
        verbose_name=_("Diğer Hayvanlar"),
        help_text=_("Evde başka hayvan var mı? Varsa neler?")
    )
    
    # Güvenlik ve tercihler
    kimlik_dogrulandi_mi = models.BooleanField(
        default=False,
        verbose_name=_("Kimlik Doğrulandı"),
        help_text=_("Kimlik belgesi doğrulandı mı?")
    )
    
    referans_kisi_1 = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_("Referans Kişi 1"),
        help_text=_("İsim - Telefon")
    )
    
    referans_kisi_2 = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_("Referans Kişi 2"),
        help_text=_("İsim - Telefon")
    )
    
    class Meta:
        verbose_name = _("📋 Kullanıcı Profil Detayı")
        verbose_name_plural = _("📋 Kullanıcı Profil Detayları")
    
    def __str__(self):
        return f"{self.kullanici.tam_ad} - Profil Detayı"

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Bu modeller, her kullanıcının platformdaki dijital kimliğini oluşturur.
# Email tabanlı authentication, profil yönetimi ve güvenlik bir arada.
# 🐾 Her kullanıcı, platformun kendine özel bir hikayesi!
