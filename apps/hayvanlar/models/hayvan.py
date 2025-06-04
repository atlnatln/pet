"""
Ana hayvan modeli
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from apps.ortak.constants import PetTypes, PetGenders, PetSizes, PetAges

class Hayvan(models.Model):
    """
    Platform üzerindeki tüm hayvanlar için temel model
    Her hayvanın kendine özgü bir hikayesi ve karakteri var
    """
    # Temel bilgiler
    ad = models.CharField(
        max_length=100, 
        verbose_name=_("Hayvan Adı")
    )
    slug = models.SlugField(
        max_length=150, 
        unique=True,
        verbose_name=_("Slug"),
        help_text=_("SEO dostu URL")
    )
    tur = models.CharField(
        max_length=20, 
        choices=PetTypes.choices,
        default=PetTypes.DIGER,
        verbose_name=_("Hayvan Türü")
    )
    # İlişkili kategori
    kategori = models.ForeignKey(
        'kategoriler.Kategori',
        on_delete=models.PROTECT, 
        related_name='hayvanlar',
        verbose_name=_("Kategori"),
        null=True
    )
    # Köpek ise ırk bilgisi 
    irk = models.ForeignKey(
        'KopekIrk',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Irk"),
        help_text=_("Köpek ırkı (sadece köpekler için)")
    )
    # Hayvan detayları
    yas = models.CharField(
        max_length=20,
        choices=PetAges.CHOICES,
        verbose_name=_("Yaş"),
        blank=True, 
        null=True
    )
    cinsiyet = models.CharField(
        max_length=10,
        choices=PetGenders.CHOICES,
        default=PetGenders.UNKNOWN,
        verbose_name=_("Cinsiyet")
    )
    boyut = models.CharField(
        max_length=5,
        choices=PetSizes.CHOICES,
        blank=True,
        null=True,
        verbose_name=_("Boyut")
    )
    renk = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Renk")
    )
    
    # Karakter ve davranış özellikleri
    karakter_ozellikleri = models.JSONField(
        blank=True,
        null=True,
        verbose_name=_("Karakter Özellikleri"),
        help_text=_("Oyuncu, sakin, arkadaş canlısı vb.")
    )
    
    # Açıklamalar
    aciklama = models.TextField(
        blank=True,
        verbose_name=_("Açıklama"),
        help_text=_("Hayvanın detaylı hikayesi ve özellikleri")
    )
    
    # Konum bilgisi
    il = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("İl")
    )
    ilce = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("İlçe")
    )
    
    # Durum ve statü
    aktif = models.BooleanField(
        default=True,
        verbose_name=_("Aktif"),
        help_text=_("Hayvan listede görüntülensin mi?")
    )
    sahiplenildi = models.BooleanField(
        default=False,
        verbose_name=_("Sahiplenildi")
    )
    
    # Zaman bilgileri
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Oluşturulma Tarihi')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Güncellenme Tarihi')
    )
    
    # Etiketler (Many-to-Many ilişkisi)
    etiketler = models.ManyToManyField(
        'etiketler.Etiket',
        blank=True,
        related_name='hayvanlar',
        verbose_name=_('Etiketler')
    )

    # Sorumlu kullanıcı
    sorumlu = models.ForeignKey(
        'kullanicilar.CustomUser',
        on_delete=models.PROTECT,
        related_name='sorumlu_hayvanlar',
        verbose_name=_('Sorumlu Kişi'),
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = _("🐾 Hayvan")
        verbose_name_plural = _("🐾 Hayvanlar")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tur']),
            models.Index(fields=['aktif']),
            models.Index(fields=['sahiplenildi']),
            models.Index(fields=['il', 'kategori']),
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return f"{self.ad} ({self.get_tur_display()})"
    
    def save(self, *args, **kwargs):
        """Slug oluştur ve kategori sayaçlarını güncelle"""
        if not self.slug:
            base_slug = slugify(self.ad)
            slug = base_slug
            counter = 1
            
            while Hayvan.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
                
            self.slug = slug
        
        # Önceki kaydı kontrol et - kategori değiştiyse eski kategorinin sayacını azalt
        if self.pk:
            try:
                eski_kayit = Hayvan.objects.get(pk=self.pk)
                if eski_kayit.kategori and eski_kayit.kategori != self.kategori:
                    from apps.kategoriler.servisler import KategoriService
                    if eski_kayit.kategori:
                        KategoriService.kategori_kullanim_guncelle(eski_kayit.kategori.id)
            except Hayvan.DoesNotExist:
                pass
        
        # Kaydet
        super().save(*args, **kwargs)
        
        # Yeni kategoriyi güncelle
        if self.kategori:
            from apps.kategoriler.servisler import KategoriService
            KategoriService.kategori_kullanim_guncelle(self.kategori.id)

        # Köpek ırk-kategori senkronizasyonu
        if self.tur == PetTypes.KOPEK and self.irk:
            self._kopek_kategori_senkronizasyonu()

    def _kopek_kategori_senkronizasyonu(self):
        """Köpek ırkı için kategori senkronizasyonu"""
        from apps.kategoriler.models import Kategori
        from django.db.models import Q
            
        # Köpekler ana kategorisini bul
        kopekler_kategori = Kategori.objects.filter(
            parent__isnull=True,
            ad__iexact='Köpekler'
        ).first()
            
        if kopekler_kategori:
            # Bu köpek ırkı için alt kategori var mı kontrol et
            irk_kategori = Kategori.objects.filter(
                Q(parent=kopekler_kategori) & 
                (Q(ad__iexact=self.irk.ad) | Q(slug__icontains=self.irk.ad.lower().replace(' ', '-')))
            ).first()
                
            # Yoksa ve bu popüler bir ırk ise, oluştur
            if not irk_kategori and self.irk.populer:
                irk_kategori = Kategori.objects.create(
                    ad=self.irk.ad,
                    slug=f"kopekler-{slugify(self.irk.ad)}",
                    parent=kopekler_kategori,
                    pet_type='kopek',
                    renk_kodu=kopekler_kategori.renk_kodu,
                    aciklama=self.irk.aciklama or f"{self.irk.ad} ırkı köpekler"
                )
                
            # Kategoriyi güncelle
            if irk_kategori:
                self.kategori = irk_kategori
            else:
                # Uygun alt kategori bulunamadı, ana kategori ata
                self.kategori = kopekler_kategori
                
            # Kategori değişikliğini kaydet
            if self.kategori_id != self.kategori.id:
                super().save(update_fields=['kategori'])

    def get_absolute_url(self):
        """Detay sayfası URL'i"""
        return reverse('hayvan-detay', args=[self.slug])
    
    @property
    def kapak_fotografi(self):
        """Kapak fotoğrafı veya ilk fotoğraf"""
        try:
            kapak = self.fotograflar.filter(kapak_fotografi=True).first()
            if kapak:
                return kapak
            return self.fotograflar.first()
        except:
            return None
    
    @property
    def fotograf_sayisi(self):
        """Fotoğraf sayısı"""
        return self.fotograflar.count()
    
    @property
    def yas_metni(self):
        """Yaşı okunabilir formatta döndürür"""
        return PetAges.get_label(self.yas)
    
    @property
    def asilar_tam_mi(self):
        """Tüm aşıların tam olup olmadığını kontrol eder"""
        if hasattr(self, 'saglik'):
            return bool(self.saglik.guncel_asilar)
        return False
