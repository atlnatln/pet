"""
🐾 Evcil Hayvan Platformu - Hayvanlar Modeli
==============================================================================
Platform üzerindeki tüm hayvanların veri yapısı ve detayları
==============================================================================
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from apps.ortak.constants import PetTypes, PetGenders, PetSizes, PetAges
from .managers import HayvanManager  # Bu import'u ekle


class KopekIrk(models.Model):
    """
    Köpek ırkları modeli
    Köpek ırklarının detaylı bilgilerini içerir
    """
    id = models.CharField(max_length=10, primary_key=True)
    ad = models.CharField(max_length=100, verbose_name="Irk Adı")
    aciklama = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    populer = models.BooleanField(default=False, verbose_name="Popüler Irk")
    yerli = models.BooleanField(default=False, verbose_name="Yerli Irk")
    aktif = models.BooleanField(default=True, verbose_name="Aktif")
    
    class Meta:
        verbose_name = "🐕 Köpek Irkı"
        verbose_name_plural = "🐕 Köpek Ansiklopedisi"
        ordering = ['ad']
    
    def __str__(self):
        return self.ad
    
    def save(self, *args, **kwargs):
        """Köpek ırkı bilgilerini kaydet ve gerekiyorsa kategori oluştur"""
        # Önce kaydet
        super().save(*args, **kwargs)
        
        # Eğer popüler ırk olarak işaretlendiyse ve aktifse kategori sistemiyle senkronize et
        if self.aktif and self.populer:
            self.kategori_ile_senkronize_et()
    
    def kategori_ile_senkronize_et(self):
        """Köpek ırkını kategori sistemiyle senkronize et"""
        try:
            # İlgili modülleri import et
            from django.utils.text import slugify
            from apps.kategoriler.models import Kategori
            
            # Ana köpek kategorisini bul
            kopekler_kategori = Kategori.objects.filter(
                ad__iexact='Köpekler', 
                parent__isnull=True
            ).first()
            
            if kopekler_kategori:
                # Bu ırk için alt kategori var mı?
                alt_kategori = Kategori.objects.filter(
                    parent=kopekler_kategori,
                    ad__iexact=self.ad
                ).first()
                
                # Alt kategori yoksa oluştur
                if not alt_kategori:
                    slug = f"kopekler-{slugify(self.ad)}"
                    
                    # Aynı slug varsa sayı ekle
                    counter = 1
                    test_slug = slug
                    while Kategori.objects.filter(slug=test_slug).exists():
                        test_slug = f"{slug}-{counter}"
                        counter += 1
                    
                    # Yeni alt kategori oluştur - pet_type düzelt
                    Kategori.objects.create(
                        ad=self.ad,
                        slug=test_slug,
                        parent=kopekler_kategori,
                        pet_type='kopek',  # 'dog' yerine 'kopek' kullan
                        renk_kodu=kopekler_kategori.renk_kodu or '#f59e0b',
                        aciklama=self.aciklama or f"{self.ad} ırkı köpekler",
                        aktif=True,
                        sira=Kategori.objects.filter(parent=kopekler_kategori).count() + 1
                    )
                elif not alt_kategori.aktif and self.aktif:
                    # Irk aktifse ama kategori pasifse, kategoriyi aktifleştir
                    alt_kategori.aktif = True
                    alt_kategori.save(update_fields=['aktif'])
                
        except Exception as e:
            # Hata durumunda sessizce devam et, kritik bir işlem değil
            # Log eklenebilir
            import logging
            logging.warning(f"Köpek ırkı kategori senkronizasyonu sırasında hata: {e}")


class HayvanFotograf(models.Model):
    """
    Hayvan fotoğrafları modeli
    Birden fazla fotoğraf desteği ve thumbnail işlemleri için
    """
    hayvan = models.ForeignKey(
        'Hayvan', 
        on_delete=models.CASCADE, 
        related_name='fotograflar',
        verbose_name=_("Hayvan")
    )
    fotograf = models.ImageField(
        upload_to='hayvanlar/fotograflar/%Y/%m/',
        verbose_name=_("Fotoğraf")
    )
    thumbnail = models.ImageField(
        upload_to='hayvanlar/thumbnails/%Y/%m/',
        blank=True,
        null=True,
        verbose_name=_("Küçük Resim")
    )
    kapak_fotografi = models.BooleanField(
        default=False,
        verbose_name=_("Kapak Fotoğrafı")
    )
    sira = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Sıra")
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Oluşturulma Tarihi")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Güncellenme Tarihi")
    )
    
    class Meta:
        verbose_name = _("🖼️ Hayvan Fotoğrafı")
        verbose_name_plural = _("🖼️ Hayvan Fotoğrafları")
        ordering = ['sira', '-created_at']
    
    def __str__(self):
        return f"{self.hayvan.ad} - Fotoğraf {self.id}"
    
    def save(self, *args, **kwargs):
        """Fotoğrafı kaydederken thumbnail oluştur"""
        super().save(*args, **kwargs)
        if not self.thumbnail:
            from apps.hayvanlar.utils import create_thumbnail
            self.thumbnail = create_thumbnail(self.fotograf)
            super().save(update_fields=['thumbnail'])


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
        KopekIrk,
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
    kisirlastirilmis = models.BooleanField(
        default=False,
        verbose_name=_("Kısırlaştırılmış")
    )
    asilar_tamam = models.BooleanField(
        default=False,
        verbose_name=_("Aşıları Tam")
    )
    mikrocipli = models.BooleanField(
        default=False,
        verbose_name=_("Mikroçipli")
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
    
    # Konum bilgisi - İl seçimi için choices ekle
    il = models.CharField(
        max_length=50,
        blank=True,
        choices=[('', '------')] + [
            ('istanbul', 'İstanbul'),
            ('ankara', 'Ankara'),
            ('izmir', 'İzmir'),
            ('bursa', 'Bursa'),
            ('antalya', 'Antalya'),
            ('konya', 'Konya'),
            ('adana', 'Adana'),
            ('gaziantep', 'Gaziantep'),
            ('mersin', 'Mersin'),
            ('kayseri', 'Kayseri'),
            # Daha fazla il eklenebilir
        ],
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
    
    # Custom manager ekle
    objects = HayvanManager()
    
    class Meta:
        verbose_name = _("🐾 Hayvan")
        verbose_name_plural = _("🐾 Hayvanlar")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tur']),
            models.Index(fields=['aktif']),
            models.Index(fields=['sahiplenildi']),
        ]
    
    def __str__(self):
        return self.ad
    
    def save(self, *args, **kwargs):
        """Slug oluştur"""
        if not self.slug:
            from django.utils.text import slugify
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
                    # Eski kategorinin kullanım sayısını güncelle (ilanlar hazır olduktan sonra)
                    pass
            except Hayvan.DoesNotExist:
                pass
    
        # Kaydet
        super().save(*args, **kwargs)
        
        # Eğer tür köpek ise ve bir ırk seçildiyse, otomatik olarak uygun kategoriyi bul veya oluştur
        if self.tur == 'kopek' and self.irk:
            try:
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
                        from django.utils.text import slugify
                        irk_kategori = Kategori.objects.create(
                            ad=self.irk.ad,
                            slug=f"kopekler-{slugify(self.irk.ad)}",
                            parent=kopekler_kategori,
                            pet_type='kopek',
                            renk_kodu=kopekler_kategori.renk_kodu,
                            aciklama=self.irk.aciklama or f"{self.irk.ad} ırkı köpekler"
                        )
                    
                    # Kategoriyi güncelle
                    if irk_kategori and not self.kategori:
                        self.kategori = irk_kategori
                        # Recursive save'i önlemek için update kullan
                        Hayvan.objects.filter(pk=self.pk).update(kategori=irk_kategori)
            except Exception as e:
                # Import hatalarını sessizce geç
                pass

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