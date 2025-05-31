"""
🐾 Kategoriler Modelleri
==============================================================================
Her hayvan türünün dijital kimliği - Sınıflandırmanın kalbi
==============================================================================
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from django.utils.text import slugify
from django.core.cache import cache

from apps.ortak.models import TimestampedModel
from apps.ortak.constants import PetTypes
from .managers import KategoriManager


class Kategori(TimestampedModel):
    """
    Hayvan kategorileri modeli
    Her kategorinin kendine özel hikayesi ve karakteristikleri var
    """
    
    # Temel bilgiler
    ad = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)],
        verbose_name=_("Kategori Adı"),
        help_text=_("Örn: Köpek, Kedi, Golden Retriever")
    )
    
    slug = models.SlugField(
        max_length=120,
        unique=True,
        verbose_name=_("URL Slug"),
        help_text=_("SEO dostu URL için otomatik oluşur")
    )
    
    aciklama = models.TextField(
        max_length=500,
        blank=True,
        verbose_name=_("Açıklama"),
        help_text=_("Bu kategori hakkında kullanıcılara bilgi veren açıklama")
    )
    
    # Hiyerarşi yapısı
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='alt_kategoriler',
        verbose_name=_("Ana Kategori"),
        help_text=_("Bu kategori bir alt kategori ise ana kategorisini seçin")
    )
    
    # Kategori detayları
    pet_type = models.CharField(
        max_length=20,
        choices=PetTypes.choices, # CHOICES yerine choices olarak düzeltildi
        default=PetTypes.DIGER,
        verbose_name=_("Hayvan Türü"),
        help_text=_("Bu kategori hangi hayvan türü için geçerli?")
    )
    
    ikon_adi = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("İkon Adı"),
        help_text=_("FontAwesome ikon adı (ör: fa-dog, fa-cat)")
    )
    
    renk_kodu = models.CharField(
        max_length=7,
        default='#6366f1',
        verbose_name=_("Renk Kodu"),
        help_text=_("Kategori temsil rengi (HEX format)")
    )
    
    # İstatistikler
    kullanim_sayisi = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Kullanım Sayısı"),
        help_text=_("Bu kategoride kaç hayvan var")
    )
    
    # Durum bilgileri
    aktif = models.BooleanField(
        default=True,
        verbose_name=_("Aktif"),
        help_text=_("Kategori kullanıcılar tarafından görülebilir mi?")
    )
    
    sira = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Sıra"),
        help_text=_("Kategorilerin listeleme sırası")
    )
    
    # Custom manager
    objects = KategoriManager() # Bu satırı ekle/düzelt
    
    class Meta:
        verbose_name = _("🏷️ Kategori")
        verbose_name_plural = _("🏷️ Kategoriler")
        ordering = ['sira', 'ad']
        unique_together = [['ad', 'parent']]
        indexes = [
            models.Index(fields=['aktif', 'sira']),
            models.Index(fields=['parent', 'aktif']),
            models.Index(fields=['pet_type', 'aktif']),
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        if self.parent:
            return f"{self.parent.ad} > {self.ad}"
        return self.ad
    
    def save(self, *args, **kwargs):
        # Slug otomatik oluştur
        if not self.slug:
            from apps.ortak.utils import create_slug
            base_slug = create_slug(self.ad)
            slug = base_slug
            counter = 1
            
            while Kategori.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        
        super().save(*args, **kwargs)
    
    @property
    def tam_ad(self):
        """Hiyerarşik tam ad"""
        if self.parent:
            return f"{self.parent.ad} > {self.ad}"
        return self.ad
    
    @property
    def seviye(self):
        """Kategori seviyesi (0: ana, 1: alt, vs.)"""
        level = 0
        parent = self.parent
        while parent:
            level += 1
            parent = parent.parent
        return level
    
    @property
    def alt_kategori_sayisi(self):
        """Bu kategorinin alt kategori sayısı"""
        return self.alt_kategoriler.filter(aktif=True).count()
    
    @property
    def toplam_hayvan_sayisi(self):
        """Bu kategori ve alt kategorilerindeki toplam hayvan sayısı"""
        # Bu method hayvan modeli oluşturulduktan sonra implement edilecek
        total = self.kullanim_sayisi
        for alt_kategori in self.alt_kategoriler.filter(aktif=True):
            total += alt_kategori.toplam_hayvan_sayisi
        return total
    
    def get_absolute_url(self):
        """Kategori detay URL'i"""
        from django.urls import reverse
        return reverse('api:v1:kategoriler:detay', kwargs={'slug': self.slug})
    
    def get_breadcrumbs(self):
        """Breadcrumb navigasyonu için kategori yolu"""
        breadcrumbs = []
        current = self
        while current:
            breadcrumbs.append({
                'ad': current.ad,
                'slug': current.slug,
                'url': current.get_absolute_url()
            })
            current = current.parent
        return list(reversed(breadcrumbs))


class KategoriOzellik(TimestampedModel):
    """
    Kategorilere özel özellikler
    Örn: Köpekler için "ırk", Kediler için "kıl uzunluğu"
    """
    
    kategori = models.ForeignKey(
        Kategori,
        on_delete=models.CASCADE,
        related_name='ozellikler',
        verbose_name=_("Kategori")
    )
    
    ad = models.CharField(
        max_length=100,
        verbose_name=_("Özellik Adı"),
        help_text=_("Örn: Irk, Boy, Kilo, Karakter")
    )
    
    alan_tipi = models.CharField(
        max_length=20,
        choices=[
            ('text', _('Metin')),
            ('number', _('Sayı')),
            ('select', _('Seçenekli')),
            ('boolean', _('Evet/Hayır')),
            ('range', _('Aralık')),
        ],
        default='text',
        verbose_name=_("Alan Tipi")
    )
    
    secenekler = models.JSONField(
        blank=True,
        null=True,
        verbose_name=_("Seçenekler"),
        help_text=_("Seçenekli alan türü için mevcut seçenekler")
    )
    
    zorunlu = models.BooleanField(
        default=False,
        verbose_name=_("Zorunlu"),
        help_text=_("Bu özellik doldurulması zorunlu mu?")
    )
    
    aktif = models.BooleanField(
        default=True,
        verbose_name=_("Aktif")
    )
    
    sira = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Sıra")
    )
    
    class Meta:
        verbose_name = _("🔧 Kategori Özelliği")
        verbose_name_plural = _("🔧 Kategori Özellikleri")
        ordering = ['sira', 'ad']
        unique_together = [['kategori', 'ad']]
    
    def __str__(self):
        return f"{self.kategori.ad} - {self.ad}"


# ==============================================================================
# 🎨 KATEGORİ HİKAYELERİ - Her kategorinin ruhunu yansıtan açıklamalar
# ==============================================================================

KATEGORI_HIKAYELERI = {
    'kopek': {
        'baslik': "🐕 Sadakat ve Dostluğun Temsilcileri",
        'hikaye': """Her köpek bir hikaye, her çift göz bir umut. Büyük bahçelerde koşmak isteyen 
        Golden'lardan, kucakta uyumayı seven Chihuahua'lara. Her boyutta sadakat, her kalpte sevgi.""",
        'ikon': 'fa-dog',
        'renk': '#f59e0b'
    },
    'kedi': {
        'baslik': "🐱 Bağımsızlık ve Zarafetin Ustası",
        'hikaye': """Pencere kenarında güneşlenen sessiz dostlar. İran kedisinin zarafetinden sokak 
        kedisinin mücadeleci ruhuna. Her miyav, bir sevgi çağrısı.""",
        'ikon': 'fa-cat',
        'renk': '#8b5cf6'
    },
    'kus': {
        'baslik': "🦅 Özgürlüğün Renkli Elçileri",
        'hikaye': """Kanaryanın melodisinden papağanın zekasına. Kafeste değil, kalplerde yaşamayı 
        seven kanatlı dostlar. Her şarkı, bir umut türküsü.""",
        'ikon': 'fa-dove',
        'renk': '#06b6d4'
    },
    'balik': {
        'baslik': "🐠 Sessiz Güzelliğin Temsilcileri",
        'hikaye': """Akvaryumda dans eden rengarenk dostlar. Goldfish'in sakinliğinden tropik 
        balıkların canlılığına. Suda yaşayan, kalplerde yer eden arkadaşlar.""",
        'ikon': 'fa-fish',
        'renk': '#3b82f6'
    },
    'kemirgen': {
        'baslik': "🐹 Minik Dostların Büyük Kalpleri",
        'hikaye': """Hamsterın sevimli çılgınlığından tavşanın uslu duruşuna. Küçük bedenler, 
        büyük sevgiler. Her bir minik parmak izi, bir mutluluk kaynağı.""",
        'ikon': 'fa-rabbit',
        'renk': '#f97316'
    },
    'surunben': {
        'baslik': "🦎 Antik Dünyanın Gizemli Temsilcileri",
        'hikaye': """Kaplumbağanın bilgeliğinden iguana'nın egzotikliğine. Milyonlarca yıllık 
        evrim, modern evlerin sakin köşelerinde yaşıyor.""",
        'ikon': 'fa-turtle',
        'renk': '#059669'
    },
    'egzotik': {
        'baslik': "🦜 Farklılığın Renkli Dünyası",
        'hikaye': """Papağanın zekasindan chinchilla'nın yumuşaklığına. Sıradışı dostlar, 
        sıradışı sevgiler. Her biri eşsiz, her biri özel.""",
        'ikon': 'fa-paw',
        'renk': '#dc2626'
    }
}

# ==============================================================================
# 💝 PLATFORM MESSAGE
# ==============================================================================

# Bu model, hayvan türlerinin dijital kimliğini oluşturur.
# Her kategori, platformdaki canlıların hikayesinin başlığıdır.
# 🐾 Her kategori, bir hayvan türünün dijital evi!
