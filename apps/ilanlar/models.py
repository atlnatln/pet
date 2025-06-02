"""
🐾 İlanlar Modelleri
==============================================================================
Sahiplendirme ve barınak ilanlarının veri yapısı
==============================================================================
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.ortak.models import TimestampedModel
from apps.ortak.constants import PetTypes
from .managers import IlanManager


class IlanDurum:
    """İlan durumları"""
    AKTIF = 'aktif'
    BEKLEMEDE = 'beklemede'
    TAMAMLANDI = 'tamamlandi'
    IPTAL = 'iptal'
    
    CHOICES = [
        (AKTIF, _('Aktif')),
        (BEKLEMEDE, _('Onay Bekliyor')),
        (TAMAMLANDI, _('Tamamlandı')),
        (IPTAL, _('İptal Edildi')),
    ]


class IlanTuru:
    """İlan türleri"""
    SAHIPLENDIRME = 'sahiplendirme'
    KAYIP = 'kayip'
    BULUNDU = 'bulundu'
    BARANAK = 'baranak'
    GEÇICI_BAKICI = 'gecici_bakici'
    
    CHOICES = [
        (SAHIPLENDIRME, _('Sahiplendirme')),
        (KAYIP, _('Kayıp Hayvan')),
        (BULUNDU, _('Bulunan Hayvan')),
        (BARANAK, _('Barınak İlanı')),
        (GEÇICI_BAKICI, _('Geçici Bakıcı Aranıyor')),
    ]


class Ilan(TimestampedModel):
    """
    Sahiplendirme ve barınak ilanları ana modeli
    """
    # Temel bilgiler
    baslik = models.CharField(
        max_length=200,
        verbose_name=_("İlan Başlığı"),
        help_text=_("Örn: 'Sevimli Golden Retriever yuva arıyor'")
    )
    
    slug = models.SlugField(
        max_length=220,
        unique=True,
        verbose_name=_("URL Slug"),
        help_text=_("SEO dostu URL için otomatik oluşur")
    )
    
    aciklama = models.TextField(
        verbose_name=_("İlan Açıklaması"),
        help_text=_("Hayvanın hikayesi, karakteri ve özel ihtiyaçları")
    )
    
    # İlan türü ve durumu
    ilan_turu = models.CharField(
        max_length=20,
        choices=IlanTuru.CHOICES,
        default=IlanTuru.SAHIPLENDIRME,
        verbose_name=_("İlan Türü")
    )
    
    durum = models.CharField(
        max_length=20,
        choices=IlanDurum.CHOICES,
        default=IlanDurum.BEKLEMEDE,
        verbose_name=_("İlan Durumu")
    )
    
    # Hayvan bilgileri
    hayvan = models.ForeignKey(
        'hayvanlar.Hayvan',
        on_delete=models.CASCADE,
        related_name='ilanlar',
        verbose_name=_("Hayvan"),
        null=True,
        blank=True
    )
    
    # İlan sahibi bilgileri (şimdilik basit, sonra kullanıcı sistemi eklenecek)
    ilan_veren_adi = models.CharField(
        max_length=100,
        verbose_name=_("İlan Veren Adı")
    )
    
    ilan_veren_telefon = models.CharField(
        max_length=20,
        verbose_name=_("Telefon")
    )
    
    ilan_veren_email = models.EmailField(
        verbose_name=_("E-posta"),
        blank=True
    )
    
    # Konum bilgisi
    il = models.CharField(
        max_length=50,
        verbose_name=_("İl")
    )
    
    ilce = models.CharField(
        max_length=50,
        verbose_name=_("İlçe")
    )
    
    adres_detay = models.TextField(
        blank=True,
        verbose_name=_("Adres Detayı"),
        help_text=_("Mahalle, sokak vb. detay bilgiler")
    )
    
    # İlan özellikleri
    acil = models.BooleanField(
        default=False,
        verbose_name=_("Acil İlan"),
        help_text=_("Acil durumda olan hayvanlar için")
    )
    
    ucretsiz = models.BooleanField(
        default=True,
        verbose_name=_("Ücretsiz"),
        help_text=_("Sahiplendirme ücretsiz mi?")
    )
    
    ucret = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Ücret"),
        help_text=_("Varsa sahiplendirme ücreti")
    )
    
    # Özel şartlar
    ozel_sartlar = models.TextField(
        blank=True,
        verbose_name=_("Özel Şartlar"),
        help_text=_("Sahiplendirme için özel şartlar varsa")
    )
    
    # İstatistikler
    goruntulenme_sayisi = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Görüntülenme Sayısı")
    )
    
    favori_sayisi = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Favori Sayısı")
    )
    
    # Tarihler
    yayinlanma_tarihi = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Yayınlanma Tarihi")
    )
    
    son_gecerlilik_tarihi = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Son Geçerlilik Tarihi")
    )
    
    # Moderasyon
    moderator_notu = models.TextField(
        blank=True,
        verbose_name=_("Moderatör Notu")
    )
    
    objects = IlanManager()
    
    class Meta:
        verbose_name = _("📢 İlan")
        verbose_name_plural = _("📢 İlanlar")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['durum', 'ilan_turu']),
            models.Index(fields=['il', 'ilce']),
            models.Index(fields=['acil', 'durum']),
            models.Index(fields=['yayinlanma_tarihi']),
        ]
    
    def __str__(self):
        return self.baslik
    
    def save(self, *args, **kwargs):
        # Slug oluştur
        if not self.slug:
            base_slug = slugify(self.baslik)
            slug = base_slug
            counter = 1
            
            while Ilan.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
                
            self.slug = slug
        
        # İlan aktif hale gelirse yayınlanma tarihini set et
        if self.durum == IlanDurum.AKTIF and not self.yayinlanma_tarihi:
            self.yayinlanma_tarihi = timezone.now()
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """İlan detay URL'i"""
        return reverse('ilan-detay', args=[self.slug])
    
    @property
    def aktif_mi(self):
        """İlan aktif mi?"""
        return self.durum == IlanDurum.AKTIF
    
    @property
    def süresi_dolmus_mu(self):
        """İlan süresi dolmuş mu?"""
        if self.son_gecerlilik_tarihi:
            return timezone.now() > self.son_gecerlilik_tarihi
        return False
    
    @property
    def ilan_turu_display(self):
        """İlan türü gösterim adı"""
        return dict(IlanTuru.CHOICES).get(self.ilan_turu, self.ilan_turu)
    
    @property
    def durum_badge_class(self):
        """Durum badge CSS class'ı"""
        badge_classes = {
            IlanDurum.AKTIF: 'success',
            IlanDurum.BEKLEMEDE: 'warning',
            IlanDurum.TAMAMLANDI: 'info',
            IlanDurum.IPTAL: 'danger',
        }
        return badge_classes.get(self.durum, 'secondary')


class IlanFotograf(TimestampedModel):
    """
    İlan fotoğrafları
    """
    ilan = models.ForeignKey(
        Ilan,
        on_delete=models.CASCADE,
        related_name='fotograflar',
        verbose_name=_("İlan")
    )
    
    fotograf = models.ImageField(
        upload_to='ilanlar/fotograflar/%Y/%m/',
        verbose_name=_("Fotoğraf")
    )
    
    thumbnail = models.ImageField(
        upload_to='ilanlar/thumbnails/%Y/%m/',
        blank=True,
        null=True,
        verbose_name=_("Küçük Resim")
    )
    
    kapak_fotografi = models.BooleanField(
        default=False,
        verbose_name=_("Kapak Fotoğrafı")
    )
    
    aciklama = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Fotoğraf Açıklaması")
    )
    
    sira = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Sıra")
    )
    
    class Meta:
        verbose_name = _("📸 İlan Fotoğrafı")
        verbose_name_plural = _("📸 İlan Fotoğrafları")
        ordering = ['sira', '-created_at']
    
    def __str__(self):
        return f"{self.ilan.baslik} - Fotoğraf {self.id}"


class IlanBasvuru(TimestampedModel):
    """
    İlanlara yapılan başvurular
    """
    ilan = models.ForeignKey(
        Ilan,
        on_delete=models.CASCADE,
        related_name='basvurular',
        verbose_name=_("İlan")
    )
    
    basvuran_adi = models.CharField(
        max_length=100,
        verbose_name=_("Başvuran Adı")
    )
    
    basvuran_telefon = models.CharField(
        max_length=20,
        verbose_name=_("Telefon")
    )
    
    basvuran_email = models.EmailField(
        verbose_name=_("E-posta")
    )
    
    mesaj = models.TextField(
        verbose_name=_("Mesaj"),
        help_text=_("Neden bu hayvanı sahiplenmek istiyorsunuz?")
    )
    
    durum = models.CharField(
        max_length=20,
        choices=[
            ('beklemede', _('Beklemede')),
            ('onaylandi', _('Onaylandı')),
            ('reddedildi', _('Reddedildi')),
        ],
        default='beklemede',
        verbose_name=_("Başvuru Durumu")
    )
    
    ilan_veren_notu = models.TextField(
        blank=True,
        verbose_name=_("İlan Veren Notu")
    )
    
    class Meta:
        verbose_name = _("📝 İlan Başvurusu")
        verbose_name_plural = _("📝 İlan Başvuruları")
        ordering = ['-created_at']
        unique_together = [['ilan', 'basvuran_email']]
    
    def __str__(self):
        return f"{self.ilan.baslik} - {self.basvuran_adi}"


class IlanRapor(TimestampedModel):
    """
    İlan raporlama sistemi
    """
    ilan = models.ForeignKey(
        Ilan,
        on_delete=models.CASCADE,
        related_name='raporlar',
        verbose_name=_("İlan")
    )
    
    rapor_eden_email = models.EmailField(
        verbose_name=_("Rapor Eden E-posta")
    )
    
    rapor_nedeni = models.CharField(
        max_length=50,
        choices=[
            ('yanlis_bilgi', _('Yanlış Bilgi')),
            ('spam', _('Spam')),
            ('uygunsuz_icerik', _('Uygunsuz İçerik')),
            ('dolandiricilik', _('Dolandırıcılık')),
            ('diger', _('Diğer')),
        ],
        verbose_name=_("Rapor Nedeni")
    )
    
    aciklama = models.TextField(
        verbose_name=_("Açıklama")
    )
    
    durum = models.CharField(
        max_length=20,
        choices=[
            ('inceleniyor', _('İnceleniyor')),
            ('cozuldu', _('Çözüldü')),
            ('gecersiz', _('Geçersiz')),
        ],
        default='inceleniyor',
        verbose_name=_("Rapor Durumu")
    )
    
    moderator_notu = models.TextField(
        blank=True,
        verbose_name=_("Moderatör Notu")
    )
    
    class Meta:
        verbose_name = _("🚨 İlan Raporu")
        verbose_name_plural = _("🚨 İlan Raporları")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.ilan.baslik} - {self.get_rapor_nedeni_display()}"
