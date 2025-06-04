"""
Hayvanların sağlık durumlarını tutan model
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class SaglikDurumu(models.Model):
    """
    Hayvanların sağlık durumu için ayrı bir model
    Aşılar, tedaviler ve genel sağlık bilgisi
    """
    ASILAR = [
        ('karma', _('Karma Aşı')),
        ('kuduz', _('Kuduz Aşısı')),
        ('parazit', _('İç/Dış Parazit')),
        ('mantar', _('Mantar Aşısı')),
        ('bronshine', _('Bronşit Aşısı')),
        ('lösemi', _('Lösemi Aşısı')),
    ]

    hayvan = models.OneToOneField(
        'Hayvan',
        on_delete=models.CASCADE,
        related_name='saglik',
        verbose_name=_('Hayvan')
    )
    asi_gecmisi = models.JSONField(
        verbose_name=_('Aşı Geçmişi'),
        help_text=_('Her aşı için tarih ve notlar'),
        default=dict
    )
    kisirlastirma_tarihi = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Kısırlaştırma Tarihi')
    )
    son_kontrol = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Son Veteriner Kontrolü')
    )
    kronik_hastaliklar = models.TextField(
        blank=True,
        verbose_name=_('Kronik Hastalıklar')
    )
    tedavi_gecmisi = models.TextField(
        blank=True,
        verbose_name=_('Tedavi Geçmişi')
    )
    ozel_bakim = models.TextField(
        blank=True,
        verbose_name=_('Özel Bakım Gereksinimleri')
    )
    notlar = models.TextField(
        blank=True,
        verbose_name=_('Sağlık Notları')
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Oluşturulma Tarihi')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Güncellenme Tarihi')
    )

    class Meta:
        verbose_name = _('🏥 Sağlık Durumu')
        verbose_name_plural = _('🏥 Sağlık Durumları')
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.hayvan.ad} - Sağlık Durumu"

    @property
    def guncel_asilar(self):
        """Son 1 yıl içinde yapılan aşıları döndürür"""
        bir_yil_once = timezone.now().date() - timezone.timedelta(days=365)
        return {
            asi: tarih
            for asi, tarih in self.asi_gecmisi.items()
            if timezone.datetime.strptime(tarih, '%Y-%m-%d').date() > bir_yil_once
        }
