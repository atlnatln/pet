"""
Köpek ırkları için model
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

class KopekIrk(models.Model):
    """
    Köpek ırkları modeli
    Köpek ırklarının detaylı bilgilerini içerir
    """
    id = models.CharField(max_length=10, primary_key=True)
    ad = models.CharField(max_length=100, verbose_name=_("Irk Adı"))
    aciklama = models.TextField(blank=True, null=True, verbose_name=_("Açıklama"))
    populer = models.BooleanField(default=False, verbose_name=_("Popüler Irk"))
    yerli = models.BooleanField(default=False, verbose_name=_("Yerli Irk"))
    aktif = models.BooleanField(default=True, verbose_name=_("Aktif"))
    
    class Meta:
        verbose_name = _("🐕 Köpek Irkı")
        verbose_name_plural = _("🐕 Köpek Ansiklopedisi")
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
                    
                    # Yeni alt kategori oluştur
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
            import logging
            logging.warning(f"Köpek ırkı kategori senkronizasyonu sırasında hata: {e}")
