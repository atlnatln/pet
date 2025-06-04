"""
🏷️ Evcil Hayvan Platformu - Etiketler Modeli
==============================================================================
Platform üzerindeki etiketlerin veri yapısı ve ilişkileri
==============================================================================
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.db.models import Count


class EtiketManager(models.Manager):
    """
    Etiket modeli için özel sorgu yöneticisi
    """
    
    def get_queryset(self):
        """Sadece aktif etiketleri döndür"""
        return super().get_queryset().filter(aktif=True)
    
    def en_populer(self, limit=10):
        """En çok kullanılan etiketleri döndür"""
        return self.annotate(
            hayvan_sayi=Count('hayvanlar', distinct=True),
            ilan_sayi=Count('ilanlar', distinct=True)
        ).order_by('-hayvan_sayi', '-ilan_sayi')[:limit]
    
    def harf_ile_baslayan(self, harf):
        """Belirli bir harfle başlayan etiketleri döndür"""
        return self.filter(ad__istartswith=harf).order_by('ad')
    
    def ile_ilgili(self, etiket_adi, limit=5):
        """Verilen etiket ile ilişkili diğer etiketleri döndür"""
        try:
            etiket = self.get(ad__iexact=etiket_adi)
            # İlişkili hayvanlar üzerinden ortak etiketleri bul
            return self.filter(hayvanlar__in=etiket.hayvanlar.all()).exclude(
                id=etiket.id
            ).annotate(
                kullanim=Count('id')
            ).order_by('-kullanim')[:limit]
        except self.model.DoesNotExist:
            return self.none()


class Etiket(models.Model):
    """
    Hayvanları ve ilanları kategorize etmek için etiket modeli
    """
    ad = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name=_("Etiket Adı"),
        help_text=_("Etiket adı benzersiz olmalıdır")
    )
    slug = models.SlugField(
        max_length=60, 
        unique=True, 
        verbose_name=_("URL Slug"),
        help_text=_("SEO dostu URL")
    )
    aciklama = models.TextField(
        blank=True,
        verbose_name=_("Açıklama"),
        help_text=_("Etiket hakkında kısa bir açıklama")
    )
    renk_kodu = models.CharField(
        max_length=7,
        default="#3B82F6", # Varsayılan mavi renk
        verbose_name=_("Renk Kodu"),
        help_text=_("Etiketin görsel temsili için HEX renk kodu (örn: #3B82F6)")
    )
    ikon = models.CharField(
        max_length=30,
        blank=True,
        verbose_name=_("İkon"),
        help_text=_("Etiket için isteğe bağlı ikon adı (Font Awesome)")
    )
    aktif = models.BooleanField(
        default=True,
        verbose_name=_("Aktif"),
        help_text=_("Etiketin aktif olup olmadığı")
    )
    olusturma_tarihi = models.DateTimeField(
        default=timezone.now, 
        verbose_name=_("Oluşturulma Tarihi")
    )
    guncelleme_tarihi = models.DateTimeField(
        auto_now=True, 
        verbose_name=_("Güncellenme Tarihi")
    )
    
    # Etiketler için özel yönetici tanımlama
    objects = EtiketManager()
    # Tüm etiketleri içeren temel yönetici (aktif olmayan etiketler dahil)
    tum_etiketler = models.Manager()
    
    class Meta:
        verbose_name = _("🏷️ Etiket")
        verbose_name_plural = _("🏷️ Etiketler")
        ordering = ['ad']  # Alfabetik sıralama
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['aktif']),
        ]
    
    def __str__(self):
        return self.ad
    
    def save(self, *args, **kwargs):
        """Slug alanını otomatik doldur"""
        if not self.slug:
            self.slug = self._generate_unique_slug()
        
        # Aynı ada sahip etiket var mı kontrol et (büyük/küçük harf duyarsız)
        if not self.pk:  # Sadece yeni etiketler için kontrol et
            existing = Etiket.tum_etiketler.filter(ad__iexact=self.ad).first()
            if existing:
                # Varolan etiket pasif durumdaysa, onu aktifleştir
                if not existing.aktif:
                    existing.aktif = True
                    existing.save()
                # Bu kaydı oluşturma, var olanı kullan
                return existing
                
        # Kaydı gerçekleştir
        super().save(*args, **kwargs)
    
    def clean(self):
        """Veri doğrulama kuralları"""
        # Renk kodu kontrolü
        if self.renk_kodu and not self.renk_kodu.startswith('#'):
            raise ValidationError({'renk_kodu': _('Renk kodu # ile başlamalıdır')})
        
    def _generate_unique_slug(self):
        """Benzersiz slug oluştur"""
        slug = slugify(self.ad)
        unique_slug = slug
        num = 1
        
        while Etiket.tum_etiketler.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
            
        return unique_slug
    
    @property
    def kullanim_sayisi(self):
        """Etiketin toplam kullanım sayısını döndür"""
        hayvan_sayisi = getattr(self, 'hayvanlar', None)
        ilan_sayisi = getattr(self, 'ilanlar', None)
        
        toplam = 0
        if hayvan_sayisi:
            toplam += hayvan_sayisi.count()
        if ilan_sayisi:
            toplam += ilan_sayisi.count()
            
        return toplam