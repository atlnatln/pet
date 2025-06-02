"""
🏷️ Etiket Uygulaması - Modeller
==============================================================================
Her hayvanın ruhunu ve karakterini yansıtan dijital etiketler sistemi
==============================================================================
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from django.utils.text import slugify
from django.core.cache import cache
from django.db.models import Count

from apps.ortak.models import TimestampedModel
from .managers import EtiketManager


class EtiketKategori(TimestampedModel):
    """
    Etiket kategorileri - Etiketleri gruplandırmak için
    Örn: 'Karakter', 'Yaşam Tarzı', 'Sağlık', 'Sosyal Özellikler'
    """
    
    ad = models.CharField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(2)],
        verbose_name=_("Kategori Adı"),
        help_text=_("Örn: Karakter, Yaşam Tarzı, Sağlık Durumu")
    )
    
    slug = models.SlugField(
        max_length=60,
        unique=True,
        verbose_name=_("URL Slug"),
        help_text=_("SEO dostu URL için otomatik oluşur")
    )
    
    aciklama = models.TextField(
        max_length=300,
        blank=True,
        verbose_name=_("Açıklama"),
        help_text=_("Bu kategori hangi tür etiketleri içerir?")
    )
    
    ikon_adi = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("İkon Adı"),
        help_text=_("FontAwesome ikon adı (ör: fa-heart, fa-home)")
    )
    
    renk_kodu = models.CharField(
        max_length=7,
        default='#6366f1',
        verbose_name=_("Renk Kodu"),
        help_text=_("Kategori temsil rengi (HEX format)")
    )
    
    sira = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Sıra"),
        help_text=_("Kategorilerin görüntülenme sırası")
    )
    
    aktif = models.BooleanField(
        default=True,
        verbose_name=_("Aktif")
    )
    
    class Meta:
        verbose_name = _("🗂️ Etiket Kategorisi")
        verbose_name_plural = _("🗂️ Etiket Kategorileri")
        ordering = ['sira', 'ad']
        indexes = [
            models.Index(fields=['aktif', 'sira']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from apps.ortak.utils import create_slug
            self.slug = create_slug(self.ad)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.ad


class Etiket(TimestampedModel):
    """
    Ana etiket modeli - Her hayvanın karakteristik özelliklerini tanımlayan
    dijital kimlik parçaları
    """
    
    # Temel kimlik bilgileri
    ad = models.CharField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(2)],
        verbose_name=_("Etiket Adı"),
        help_text=_("Örn: Oyuncu, Sakin, Çocuk Dostu, Apartman Yaşamına Uygun")
    )
    
    slug = models.SlugField(
        max_length=60,
        unique=True,
        verbose_name=_("URL Slug"),
        help_text=_("SEO dostu URL - otomatik oluşur")
    )
    
    aciklama = models.TextField(
        max_length=200,
        blank=True,
        verbose_name=_("Açıklama"),
        help_text=_("Bu etiketin ne anlama geldiğine dair kısa açıklama")
    )
    
    # Kategorizasyon
    kategori = models.ForeignKey(
        EtiketKategori,
        on_delete=models.PROTECT,
        related_name='etiketler',
        null=True,
        blank=True,
        verbose_name=_("Kategori"),
        help_text=_("Bu etiket hangi kategoriye ait?")
    )
    
    # Davranış ve görünüm
    renk_kodu = models.CharField(
        max_length=7,
        blank=True,
        verbose_name=_("Özel Renk Kodu"),
        help_text=_("Boş bırakılırsa kategori rengi kullanılır")
    )
    
    populer = models.BooleanField(
        default=False,
        verbose_name=_("Popüler Etiket"),
        help_text=_("Sık kullanılan etiketler için işaretleyin")
    )
    
    oncelik = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Öncelik"),
        help_text=_("Yüksek öncelikli etiketler önce görüntülenir")
    )
    
    # İstatistikler
    kullanim_sayisi = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Kullanım Sayısı"),
        help_text=_("Bu etiketi kullanan ilan sayısı - otomatik güncellenir")
    )
    
    # Durum
    aktif = models.BooleanField(
        default=True,
        verbose_name=_("Aktif"),
        help_text=_("Etiket kullanılabilir durumda mı?")
    )
    
    onay_bekliyor = models.BooleanField(
        default=False,
        verbose_name=_("Onay Bekliyor"),
        help_text=_("Kullanıcı tarafından oluşturulan etiketler için")
    )
    
    # Etiket sistemine custom manager ekleme
    objects = EtiketManager()
    
    class Meta:
        verbose_name = _("🏷️ Etiket")
        verbose_name_plural = _("🏷️ Etiketler")
        ordering = ['-populer', '-oncelik', '-kullanim_sayisi', 'ad']
        indexes = [
            models.Index(fields=['aktif', 'onay_bekliyor']),
            models.Index(fields=['populer', 'aktif']),
            models.Index(fields=['kategori', 'aktif']),
            models.Index(fields=['-kullanim_sayisi']),
            models.Index(fields=['slug']),
        ]
    
    def clean(self):
        """Model validasyonu"""
        from django.core.exceptions import ValidationError
        
        # Etiket adı normalizasyonu
        if self.ad:
            self.ad = self.ad.strip().lower().title()
        
        # Renk kodu validasyonu
        if self.renk_kodu:
            import re
            if not re.match(r'^#[0-9A-Fa-f]{6}$', self.renk_kodu):
                raise ValidationError({
                    'renk_kodu': _("Geçerli bir HEX renk kodu giriniz (örn: #ff0000)")
                })
    
    def save(self, *args, **kwargs):
        # Slug otomatik oluştur
        if not self.slug:
            from apps.ortak.utils import create_slug
            base_slug = create_slug(self.ad)
            slug = base_slug
            counter = 1
            
            while Etiket.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.ad
    
    @property
    def effective_renk(self):
        """Etkili renk - etiketin kendi rengi varsa onu, yoksa kategori rengini döner"""
        return self.renk_kodu or (self.kategori.renk_kodu if self.kategori else '#6366f1')
    
    @property
    def ilan_sayisi(self):
        """Bu etiketi kullanan aktif ilan sayısı"""
        return self.kullanim_sayisi
    
    def kullanim_istatistigi_guncelle(self):
        """Kullanım sayısını güncelle"""
        # İlanlar modeliyle entegrasyon tamamlandığında aktifleştirilecek
        try:
            from apps.ilanlar.models import Ilan
            self.kullanim_sayisi = self.ilanlar.filter(aktif=True).count()
            self.save(update_fields=['kullanim_sayisi'])
        except ImportError:
            pass
    
    def get_absolute_url(self):
        """Etiket detay URL'i"""
        from django.urls import reverse
        return reverse('api:v1:etiketler:detay', kwargs={'slug': self.slug})


# İlanlar ile Etiketler arasındaki ilişki tablosu
# Bu, ilanlar uygulamasında tanımlanacak ManyToMany ilişkisi için
# through modeli olarak kullanılabilir

class IlanEtiket(TimestampedModel):
    """
    İlan-Etiket ilişki tablosu - gelecekte ek özellikler için
    """
    
    ilan = models.ForeignKey(
        'ilanlar.Ilan',  # String reference - circular import'u önler
        on_delete=models.CASCADE,
        verbose_name=_("İlan")
    )
    
    etiket = models.ForeignKey(
        Etiket,
        on_delete=models.CASCADE,
        verbose_name=_("Etiket")
    )
    
    # Gelecekte eklenebilecek ek özellikler
    onem_derecesi = models.PositiveIntegerField(
        default=1,
        choices=[
            (1, _('Normal')),
            (2, _('Önemli')),
            (3, _('Çok Önemli')),
        ],
        verbose_name=_("Önem Derecesi"),
        help_text=_("Bu etiketin bu ilan için ne kadar önemli olduğu")
    )
    
    ekleme_nedeni = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Ekleme Nedeni"),
        help_text=_("Bu etiketin neden eklendiğine dair not")
    )
    
    class Meta:
        verbose_name = _("🔗 İlan-Etiket İlişkisi")
        verbose_name_plural = _("🔗 İlan-Etiket İlişkileri")
        unique_together = [['ilan', 'etiket']]
        indexes = [
            models.Index(fields=['ilan', 'etiket']),
            models.Index(fields=['etiket', 'onem_derecesi']),
        ]
    
    def __str__(self):
        return f"{self.ilan} - {self.etiket}"


# ==============================================================================
# 💝 ETIKET HİKAYELERİ - Etiket kategorilerinin karakteristikleri
# ==============================================================================

ETIKET_KATEGORI_HIKAYELERI = {
    'karakter': {
        'baslik': "💝 Karakter Özellikleri",
        'hikaye': "Her hayvanın kendine özgü karakteri vardır. Oyuncu, sakin, enerjik veya uysal - her karakter farklı bir hikaye anlatır.",
        'ikon': 'fa-heart',
        'renk': '#e74c3c',
        'ornek_etiketler': ['oyuncu', 'sakin', 'enerjik', 'uysal', 'meraklı', 'bağımsız']
    },
    'yasam_tarzi': {
        'baslik': "🏠 Yaşam Tarzı Uyumluluğu",
        'hikaye': "Hayvanların yaşam alanı ihtiyaçları ve uyum sağlayabilecekleri ortamlar.",
        'ikon': 'fa-home',
        'renk': '#3498db',
        'ornek_etiketler': ['apartman_uygun', 'bahçe_gerekir', 'şehir_hayatı', 'kırsal_alan']
    },
    'sosyal': {
        'baslik': "👥 Sosyal Özellikler",
        'hikaye': "Hayvanların diğer canlılarla ve insanlarla olan etkileşim yetenekleri.",
        'ikon': 'fa-users',
        'renk': '#2ecc71',
        'ornek_etiketler': ['çocuk_dostu', 'diğer_hayvanlarla_uyumlu', 'yalnız_yaşamayı_tercih_eder']
    },
    'saglik': {
        'baslik': "🏥 Sağlık ve Bakım",
        'hikaye': "Sağlık durumu, özel bakım gereksinimleri ve tıbbi özellikler.",
        'ikon': 'fa-medical-bag',
        'renk': '#9b59b6',
        'ornek_etiketler': ['kısırlaştırılmış', 'aşıları_tam', 'özel_bakım_gerekir', 'hipoalerjenik']
    },
    'egitim': {
        'baslik': "🎓 Eğitim Durumu",
        'hikaye': "Hayvanların eğitim seviyesi ve öğrenme yetenekleri.",
        'ikon': 'fa-graduation-cap',
        'renk': '#f39c12',
        'ornek_etiketler': ['tuvalet_eğitimi_almış', 'temel_komutlar_biliyor', 'eğitime_açık']
    }
}

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Bu model yapısı, etiket sisteminin temelini oluşturur.
# Her etiket, hayvanların hikayesinin bir parçasıdır.
# 🏷️ Etiketler, hayvan ve insan arasındaki uyumun anahtarıdır!
