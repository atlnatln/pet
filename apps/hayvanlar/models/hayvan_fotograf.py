"""
Hayvan fotoğrafları için model
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

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
